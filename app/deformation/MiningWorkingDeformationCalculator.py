from app.deformation.DeformationCalculatorABC import DeformationCalculatorABC
from app.deformation.DeformationPoint import DeformationPoint
from app.mine_workings.MineWorking import MineWorking


class MiningWorkingDeformationCalculator(DeformationCalculatorABC):
    def __init__(self, mining_working: MineWorking):
        self.mining_working = mining_working

    def calculate_deformation_for_point(self, point: DeformationPoint):
        deformation = self.mining_working.get_norm_distance_from_mw_to_point(point)
        point.deformation = deformation
