from app.deformation.DeformationPointTransformatorToFlatCSOfMW import DeformationPointTransformatorToFlatCSOfMW
from app.deformation.FlatDeformationScan import FlatDeformationScan
from app.deformation.calculators.DeformationCalculatorABC import DeformationCalculatorABC
from app.deformation.calculators.DeformationPoint import DeformationPoint


class DeformationCalculatorByFlatDefScan(DeformationCalculatorABC):

    def __init__(self, flat_def_scan: FlatDeformationScan):
        self.flat_def_scan = flat_def_scan
        self.mining_working = flat_def_scan.mining_working
        self.flat_base_point_dict = self.__init_flat_base_point_dict()
        self.point_transformator = DeformationPointTransformatorToFlatCSOfMW(self.mining_working)

    def __init_flat_base_point_dict(self):
        point_dict = {}
        for point in self.flat_def_scan:
            point_dict[f"{point.x:.3f}, {point.y:.3f}"] = point.deformation
        return point_dict

    def calculate_deformation_for_point(self, point: DeformationPoint):
        flatted_point = self.point_transformator.transform_to_flat_cs(point)
        try:
            deformation = self.flat_base_point_dict[f"{flatted_point.x:.3f}, {flatted_point.y:.3f}"]
        except (AttributeError, KeyError):
            deformation = None
        point.deformation = deformation
