import math

from app.deformation.DeformationPoint import DeformationPoint
from app.deformation.DeformationPointTransformatorToFlatCSOfMW import DeformationPointTransformatorToFlatCSOfMW
from app.deformation.DeformationScan import DeformationScan
from app.mine_workings.MineWorking import MineWorking


class FlatDeformationScan(DeformationScan):

    def __init__(self, scan_name):
        super().__init__(scan_name)
        self.base_scan = None
        self.mining_working = None

    def calculate_def_scan_by_base_obj(self):
        def_scan = DeformationScan(scan_name=f"DS_by_{self.name}")
        for point in self:
            distance_by_mine_working = point.x
            distance_by_mcs = point.y
            ms, distance_left = self.mining_working.get_ms_elm_for_distance(distance_by_mine_working)
            point_on_mcs = ms.mcs.get_point_om_mcs_dy_distance(distance_by_mcs)
            mcs_az = ms.mcs._get_angle_to_point(point=point_on_mcs)
            point_on_mcs.x += point.deformation * math.cos(mcs_az)
            point_on_mcs.y += point.deformation * math.sin(mcs_az)
            point_in_ms_cs = ms.calculate_point_on_line_form_mcs_point(mcs_point=point_on_mcs,
                                                                       distance=distance_left)
            def_point = DeformationPoint.create_def_point_from_point(point_in_ms_cs)
            def_point.deformation = point.deformation
            def_scan.add_point(def_point)
        def_scan._calk_deformation_limits()
        def_scan._calk_deformations_mse()
        return def_scan

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
        flat_def_scan._calk_deformation_limits()
        flat_def_scan._calk_deformations_mse()
        return flat_def_scan
