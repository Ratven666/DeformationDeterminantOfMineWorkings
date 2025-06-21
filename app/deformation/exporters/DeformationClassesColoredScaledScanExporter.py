from app.deformation.DeformationGMMClassificator import DeformationGMMClassificator


class DeformationClassesColoredScaledScanExporter:

    def __init__(self, file_path):
        self.file_path = file_path

    def export(self, scan):
        self._init_point_colors_by_deformation(scan)
        with open(self.file_path, "w", encoding="UTF-8") as file:
            for point in scan:
                point_str = (f"{point.x} {point.y} {point.z} {point.color[0]} {point.color[1]} "
                             f"{point.color[2]} {point.deformation} {point.deformation_class}\n")
                file.write(point_str)

    def _init_point_colors_by_deformation(self, scan):
        try:
            for point in scan:
                if point.deformation_class == 0:
                    point.color = (0, 255, 0)
                elif point.deformation_class == -1:
                    point.color = (255, 0, 0)
                elif point.deformation_class == 1:
                    point.color = (0, 0, 255)
        except AttributeError:
            print("Проводится классификация стандартным классификатором")
            dgmmc = DeformationGMMClassificator(def_scan=scan,
                                                n_of_class=3,
                                                probability_delta=0.0)
            self._init_point_colors_by_deformation(scan)
