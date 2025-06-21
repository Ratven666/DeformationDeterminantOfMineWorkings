from app.deformation.DeformationScan import DeformationScan
from app.deformation.calculators.MiningWorkingDeformationCalculator import MiningWorkingDeformationCalculator


class DeformationScanSeparatorByMW:
    def __init__(self, scan, mining_workings):
        self.mining_workings = mining_workings
        self.scan = scan
        self.def_scans = self.__init_def_scans()
        self.point_dict = {}

    def __init_def_scans(self):
        def_scans = {}
        for mw in self.mining_workings:
            def_scans[mw.name] = DeformationScan(scan_name=f"{self.scan.name}_{mw.name}")
        return def_scans

    def __calculate_def_point_dict(self):
        point_dict = {repr(point): {} for point in DeformationScan.create_def_scan_from_scan(scan=self.scan)}
        for mw in self.mining_workings:
            ds = DeformationScan.create_def_scan_from_scan(scan=self.scan)
            ds.calculate_deformation(deformation_calculator=MiningWorkingDeformationCalculator,
                                     mining_working=mw)
            for point in ds:
                try:
                    point_dict[repr(point)][mw.name] = point
                except KeyError:
                    print(point)
        self.point_dict = point_dict

    def separate_scan_by_mw(self):
        self.__init_def_scans()
        self.__calculate_def_point_dict()
        for point in self.point_dict.values():
            point_data = list(point.items())
            point_data.sort(key=lambda data: abs(data[1].deformation))
            self.def_scans[point_data[0][0]].add_point(point_data[0][1])
        for scan in self.def_scans.values():
            scan.refresh_def()
        return list(self.def_scans.values())
