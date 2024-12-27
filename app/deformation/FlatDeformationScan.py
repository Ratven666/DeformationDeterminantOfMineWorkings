from app.deformation.DeformationPoint import DeformationPoint
from app.deformation.DeformationPointTransformatorToFlatCSOfMW import DeformationPointTransformatorToFlatCSOfMW
from app.deformation.DeformationScan import DeformationScan
from app.mine_workings.MineWorking import MineWorking


class FlatDeformationScan(DeformationScan):

    def __init__(self, scan_name, def_scale=1, rbf_function="linear"):
        super().__init__(scan_name)
        self.def_scale = def_scale
        self.function = rbf_function
        self.base_scan = None
        self.mining_working = None
        self.rbf = None

    def __str__(self):
        return (f"{self.__class__.__name__} (scan_name={self.name}, "
                f"num_of_point={len(self)}, borders={self.borders})")

    @classmethod
    def create_flat_def_scan_from_mining_working_def_scan(cls, def_scan: DeformationScan,
                                                    mining_working: MineWorking,
                                                    get_point_in_mw_cs=False):
        flat_def_scan = cls(scan_name=f"Flat_DS_{def_scan.name}")
        flat_def_scan.base_scan = def_scan
        flat_def_scan.mining_working = mining_working
        point_transformator = DeformationPointTransformatorToFlatCSOfMW(mining_working)
        for point in def_scan:
            point = point_transformator.transform_to_flat_cs(point, get_point_in_mw_cs)
            if point is None:
                continue
            flat_def_scan.add_point(point)
        return flat_def_scan
