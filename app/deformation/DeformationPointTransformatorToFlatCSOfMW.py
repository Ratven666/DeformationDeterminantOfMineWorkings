from app.base.Point import Point
from app.deformation.DeformationPoint import DeformationPoint
from app.mine_workings.MineWorking import MineWorking


class DeformationPointTransformatorToFlatCSOfMW:

    def __init__(self, mining_working: MineWorking):
        self.mining_working = mining_working
        self.mcs = self.mining_working.mcs
        self.length_90 = self.mcs.get_length_on_mcs_for_point(Point(x=0, y=1000))
        self.length_180 = self.mcs.get_length_on_mcs_for_point(Point(x=-1000, y=0))
        self.length_270 = self.mcs.get_length_on_mcs_for_point(Point(x=-0, y=-1000))
        self.length_360 = self.mcs.get_length_on_mcs_for_point(Point(x=1000, y=-1e-10))


    def recalculate_point_in_ms_cs(self, point: DeformationPoint):
        mcs_distance = point.y
        if 0 < mcs_distance <= self.length_90:
            tr_y = self.length_90 - mcs_distance
        elif self.length_90 < mcs_distance <= self.length_270:
            tr_y = (mcs_distance - self.length_90) * -1
        else:
            tr_y = (self.length_360 - mcs_distance) + self.length_90
        point.y = float(tr_y)

    def transform_to_flat_cs(self, point: DeformationPoint, get_point_in_mw_cs=False):
        mw_distance = self.mining_working.get_distance_from_start_point_to_point(point)
        if mw_distance == -1:
            return None
        ms = self.mining_working.get_mining_section_to_point(point)
        tr_point = ms.transform_point_to_mcs_coord_system(point)
        try:
            mcs_distance = self.mining_working.mcs.get_length_on_mcs_for_point(tr_point)
        except ValueError:
            return None
        new_x = mw_distance
        new_y = mcs_distance
        new_z = point.deformation
        new_point = DeformationPoint(x=float(new_x),
                                     y=float(new_y),
                                     z=float(new_z),
                                     color=point.color)
        new_point.deformation = point.deformation
        if get_point_in_mw_cs:
            self.recalculate_point_in_ms_cs(new_point)
        return new_point
