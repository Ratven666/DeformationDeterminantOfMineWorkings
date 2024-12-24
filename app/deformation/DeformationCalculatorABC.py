from abc import ABC, abstractmethod

from app.deformation.DeformationPoint import DeformationPoint
from app.deformation.DeformationScan import DeformationScan


class DeformationCalculatorABC(ABC):

    @abstractmethod
    def __init__(self, *args, **kwargs):
        pass

    def calculate(self, def_scan: DeformationScan):
        for point in def_scan:
            self.calculate_deformation_for_point(point)

    @abstractmethod
    def calculate_deformation_for_point(self, point: DeformationPoint):
        pass
