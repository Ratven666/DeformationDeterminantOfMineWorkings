from app.deformation.DeformationScan import DeformationScan
from app.deformation.FlatDeformationScan import FlatDeformationScan
from app.deformation.calculators.DeformationCalculatorABC import DeformationCalculatorABC
from app.deformation.calculators.DeformationCalculatorBetweenTwoFlatDefScan import \
    DeformationCalculatorBetweenTwoFlatDefScan
from app.deformation.calculators.DeformationPoint import DeformationPoint
from app.deformation.filters.FlatDeformationScanFilterByX import FlatDeformationScanFilterByX


class ChunkDeformationCalculatorBetweenTwoFlatDefScan(DeformationCalculatorABC):

    def __init__(self, base_scan: FlatDeformationScan,
                 chunk_length=1, chunk_offsets=0.2,
                 rbf_function="linear"):
        self.base_scan = base_scan
        self.chunk_length = chunk_length
        self.chunk_offsets = chunk_offsets

        self.rbf_function = rbf_function
        # self.rbf = self.get_rbf(function=self.rbf_function)

    def __init_chunks_scans(self, def_scan: DeformationScan):
        current_x = 0
        scans_list = []
        while current_x < self.base_scan.borders["x_max"]:
            x_0 = current_x
            x_1 = current_x + self.chunk_length
            x_0_off = x_0 - self.chunk_offsets
            x_1_off = x_1 + self.chunk_offsets
            base_sub_scan = self.base_scan.filter_scan(filter_cls=FlatDeformationScanFilterByX,
                                                       replace_points_in_scan=False,
                                                       x_min=x_0_off,
                                                       x_max=x_1_off)
            def_sub_scan = def_scan.filter_scan(filter_cls=FlatDeformationScanFilterByX,
                                                replace_points_in_scan=False,
                                                x_min=x_0,
                                                x_max=x_1)
            scans_list.append([base_sub_scan, def_sub_scan])
            current_x = x_1
        return scans_list

    def __calc_deformation_in_sub_scans(self, scans_list):
        for base_scan, def_scan in scans_list:
            def_scan = DeformationScan.create_def_scan_from_scan(def_scan)
            def_scan.calculate_deformation(deformation_calculator=DeformationCalculatorBetweenTwoFlatDefScan,
                                           base_scan=base_scan,
                                           rbf_function=self.rbf_function)
            print(f"Посчитаныы деформации в скане - {def_scan}")

    def collect_full_scan(self, scans_list):
        full_def_scan = DeformationScan("Full_def_scan")
        for _, def_scan in scans_list:
            for point in def_scan:
                full_def_scan.add_point(point)
        full_def_scan.refresh_def()
        return full_def_scan

    def calculate(self, def_scan: DeformationScan):
        scans_list = self.__init_chunks_scans(def_scan=def_scan)
        self.__calc_deformation_in_sub_scans(scans_list=scans_list)
        full_def_scan = self.collect_full_scan(scans_list)
        def_scan._points = full_def_scan._points
        def_scan.borders = def_scan._get_borders_dict(def_scan._points)

    def calculate_deformation_for_point(self, point: DeformationPoint):
        pass
