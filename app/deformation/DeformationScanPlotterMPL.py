from matplotlib import pyplot as plt
from matplotlib.colors import TwoSlopeNorm

from app.scan.plotters.ScanPlotterABC import ScanPlotterABC


class DeformationScanPlotterMPL(ScanPlotterABC):

    # def __init__(self, cylinder, def_scale, plot_cylinder=True):
    #     self.cylinder = cylinder
    #     self.def_scale = def_scale
    #     self.plot_cylinder = plot_cylinder

    def __init__(self, base_obj=None, fig_ax=None, plot_base_obj=True):
        self.base_obj = base_obj
        self.plot_base_obj = plot_base_obj
        if fig_ax is None:
            self.fig = plt.figure()
            self.ax = self.fig.add_subplot(projection='3d')
        else:
            self.fig, self.ax = fig_ax

    def plot(self, scan):
        x, y, z, c = [], [], [], []
        norm = TwoSlopeNorm(vcenter=0)
        for point in scan:
            x.append(point.x)
            y.append(point.y)
            z.append(point.z)
            c.append(point.deformation)
        self.ax.scatter(x, y, z, c=c, cmap='seismic', norm=norm)
        self.ax.set_xlabel('X')
        self.ax.set_ylabel('Y')
        if self.plot_base_obj and self.base_obj is not None:
            self.base_obj.plot(fig_ax=(self.fig, self.ax), is_show=False)
        plt.axis('equal')
        plt.show()