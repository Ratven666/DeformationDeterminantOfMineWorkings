from app.deformation.DeformationPoint import DeformationPoint
from app.scan.Scan import Scan


class DeformationScan(Scan):

    def __init__(self, scan_name):
        super().__init__(scan_name)
        self.min_deformation = None
        self.max_deformation = None
        self.mse = None

    def __str__(self):
        s_str = super().__str__()
        min_deformation = round(self.min_deformation, 3) if self.min_deformation is not None else "Not Calculated"
        max_deformation = round(self.max_deformation, 3) if self.max_deformation is not None else "Not Calculated"
        mse = round(self.mse, 3) if self.mse is not None else "Not Calculated"
        return (f"{s_str}\b\b def_limits=[({min_deformation})-({max_deformation})]_"
                f"def_mse={mse}")

    def add_point(self, point):
        if isinstance(point, DeformationPoint):
            self._points.append(point)
            self.borders = self._check_border(borders_dict=self.borders, point=point)
        else:
            d_point = DeformationPoint.create_def_point_from_point(point)
            self.add_point(d_point)

    @classmethod
    def create_def_scan_from_scan(cls, scan: Scan):
        def_scan = cls(scan_name=scan.name)
        for point in scan:
            def_scan.add_point(point)
        return def_scan

    def _calk_deformation_limits(self):
        def_lst = []
        for point in self:
            def_lst.append(point.deformation)
        self.min_deformation = min(def_lst)
        self.max_deformation = max(def_lst)

    def _calk_deformations_mse(self):
        vv = []
        for point in self:
            vv.append(point.deformation ** 2)
        sum_vv = sum(vv)
        mse = (sum_vv / len(vv)) ** 0.5
        self.mse = mse

    def calculate_deformation(self, deformation_calculator, *args, **kwargs):
        deformation_calculator = deformation_calculator(*args, **kwargs)
        deformation_calculator.calculate(def_scan=self)
        self._calk_deformation_limits()
        self._calk_deformations_mse()
