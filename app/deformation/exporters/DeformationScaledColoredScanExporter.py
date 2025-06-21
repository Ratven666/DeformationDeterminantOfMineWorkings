from matplotlib import pyplot as plt
from matplotlib.colors import TwoSlopeNorm, LinearSegmentedColormap


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
    def get_c_map():
        colors = [
            (0.0, (1.0, 0.0, 0.0)),
            (0.4, (1.0, 1.0, 0.0)),
            (0.45, (0.0, 1.0, 0.0)),
            (0.55, (0.0, 1.0, 0.0)),
            (0.6, (0.0, 1.0, 1.0)),
            (1.0, (0.0, 0.0, 1.0)),
        ]
        cmap_smooth = LinearSegmentedColormap.from_list("R_Y_G_C_B", colors)
        return cmap_smooth

    def _init_point_colors_by_deformation(self, scan):
        deformation = [point.deformation for point in scan]
        norm = TwoSlopeNorm(vcenter=0, vmin=min(deformation), vmax=max(deformation))
        # colors = plt.cm.seismic(norm(deformation))
        cmap = self.get_c_map()
        colors = cmap(norm(deformation))
        for idx, point in enumerate(scan):
            color = [int(rgb * 255) for rgb in colors[idx][:3]]
            point.color = color
