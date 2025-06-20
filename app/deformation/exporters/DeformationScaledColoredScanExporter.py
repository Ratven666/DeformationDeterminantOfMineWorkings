import math
import os
from copy import deepcopy

from matplotlib import pyplot as plt
from matplotlib.colors import TwoSlopeNorm

from app.deformation.FlatDeformationScan import FlatDeformationScan
from app.deformation.DeformationScan import DeformationScan


class DeformationScaledColoredScanExporter:

    def __init__(self, file_path):
        self.file_path = file_path

    def export(self, scan):
        self._init_point_colors_by_deformation(scan)
        with open(self.file_path, "w", encoding="UTF-8") as file:
            for point in scan:
                point_str = f"{point.x} {point.y} {point.z} {point.color[0]} {point.color[1]} {point.color[2]} {point.deformation}\n"
                # point_str = f"{point.x} {point.y} {point.z} {point.color[0]} {point.color[1]} {point.color[2]}\n"
                file.write(point_str)

    @staticmethod
    def _init_point_colors_by_deformation(scan):
        deformation = [point.deformation for point in scan]
        norm = TwoSlopeNorm(vcenter=0, vmin=min(deformation), vmax=max(deformation))
        colors = plt.cm.seismic(norm(deformation))
        for idx, point in enumerate(scan):
            color = [int(rgb * 255) for rgb in colors[idx][:3]]
            point.color = color
