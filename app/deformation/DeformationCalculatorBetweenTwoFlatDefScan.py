from scipy.interpolate import Rbf


from app.deformation.DeformationCalculatorABC import DeformationCalculatorABC
from app.deformation.DeformationPoint import DeformationPoint
from app.deformation.FlatDeformationScan import FlatDeformationScan


class DeformationCalculatorBetweenTwoFlatDefScan(DeformationCalculatorABC):
    def __init__(self, base_scan=FlatDeformationScan, rbf_function="linear"):
        self.base_scan = base_scan
        self.rbf_function = rbf_function
        self.rbf = self.get_rbf(function=self.rbf_function)

    def get_rbf(self, function=None):
        x, y, z = [], [], []
        for point in self.base_scan:
            x.append(point.x)
            y.append(point.y)
            z.append(point.z)
        return Rbf(x, y, z, function=function)

    def calculate_deformation_for_point(self, point: DeformationPoint):
        base_deformation = self.rbf(point.x, point.y)
        deformation = point.deformation - base_deformation
        point.deformation = deformation
