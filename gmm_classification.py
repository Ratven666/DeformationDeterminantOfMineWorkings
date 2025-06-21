import seaborn as sns
import matplotlib.pyplot as plt

from app.deformation.DeformationScan import DeformationScan
from app.deformation.DeformationGMMClassificator import DeformationGMMClassificator
from app.deformation.exporters.DeformationClassesColoredScaledScanExporter import DeformationClassesColoredScaledScanExporter

from app.deformation.filters.DeformationScanFilterByDeformationValue import DeformationScanFilterByDeformationValue
from app.deformation.parsers.DeformationScanParserFormTxt import DeformationScanParserFormTxt
from app.scan.filters.ScanFilterDelimiter import ScanFilterDelimiter

def_scan = DeformationScan("БДШ023 16_04_25_VTO")

def_scan.load_points_from_file(parser=DeformationScanParserFormTxt,
                               file_path="src/diana/final/NEW_TOTAL_DEF_TOTAL_БДШ023 16_04_25_BDH.txt")
def_scan.filter_scan(filter_cls=DeformationScanFilterByDeformationValue, max_deformation=0.1)

# def_scan.filter_scan(filter_cls=ScanFilterDelimiter, delimiter=100)

dgmmc = DeformationGMMClassificator(def_scan=def_scan,
                                    n_of_class=3,
                                    probability_delta=0.0)

# def_scan.export_points_from_file(f"GMM_{def_scan.name}.txt", parser=DeformationClassesColoredScaledScanExporter)

dgmmc.plot_classification_result()
print(dgmmc.get_stable_zone_params_dict())


# max_def = 0.1
# def_lst = [point.deformation for point in def_scan]
# def_lst = list(filter(lambda x: abs(x) < max_def, def_lst))
#
#
#
# sns.set_style("whitegrid")  # Сетка на белом фоне
# # sns.set_palette("pastel")  # Пастельные цвета
#
# # Построение гистограммы + KDE (оценка плотности)
# plt.figure(figsize=(10, 6))
# sns.histplot(def_lst,
#              kde=False,
#              bins=100,
#              # color='royalblue',
#              # edgecolor='black',
#              )
#
# # Подписи
# plt.title('Гистограмма с оценкой плотности (KDE)', fontsize=14)
# plt.xlabel('Значение', fontsize=12)
# plt.ylabel('Частота', fontsize=12)
#
# plt.show()