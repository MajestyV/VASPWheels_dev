import os  #使用os的path模块
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import colors
from matplotlib.cm import ScalarMappable
from matplotlib.colors import LinearSegmentedColormap

class Heatmap:
    ''' This class of function is design to visualize heatmaps. '''

    # 此函数类利用matplotlib绘制热度图（https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.imshow.html）
    # 输入的数据data应为二维数组
    def __init__(self,data,show_plotting_range=True,
                 customize_colorbar=True,colorbar_name='untitled',color_list=('#072C54', '#FFFFFF'),nbins=100,
                 **kwargs):
        self.data = data

        #length, width = data.shape
        #maximum = max([[max(data[n]) for n in range(length)]

        # 动态参数传入
        self.interpolation = kwargs['interpolation'] if 'interpolation' in kwargs else 'none'  # 插值选项
        self.data_range = kwargs['mapping_range'] if 'mapping_range' in kwargs else (np.min(data),np.max(data))  # 数据范围
        self.color_norm = colors.Normalize(vmin=self.data_range[0],vmax=self.data_range[1])  # 指定数据范围归一化色值

        # 色条参数
        if  customize_colorbar:
            self.cmap = LinearSegmentedColormap.from_list(colorbar_name,color_list,N=nbins)
        else:
            self.cmap = kwargs['cmap'] if 'cmap' in kwargs else 'viridis'

        # 刻度参数
        self.tick_color = kwargs['tick_color'] if 'tick_color' in kwargs else 'k'  # 默认为黑色

        if show_plotting_range:
            print(self.data_range)
        else:
            pass

    def FigureSetting(self):
        # 改变刻度线参数
        plt.rcParams.update({'xtick.direction': 'in', 'ytick.direction': 'in'})  # 设置x轴和y轴刻度线方向向内
        plt.tick_params(bottom=True, top=False, left=True, right=False, colors=self.tick_color)
        # plt.rcParams.update({'xtick.direction': 'in', 'ytick.direction': 'in'})  # 设置x轴和y轴刻度线方向向内

    # 此函数可绘制热度图
    def ShowImage(self):
        plt.tick_params(bottom=False, top=False, left=False, right=False, colors=self.tick_color)
        plt.imshow(self.data,interpolation=self.interpolation,norm=self.color_norm,cmap=self.cmap)
        return

    # 此函数可用于展示一个colormap
    def ShowCmap(self):
        self.FigureSetting()
        cmap = ScalarMappable(norm=self.color_norm, cmap=self.cmap)
        fig, ax = plt.subplots(figsize=(6, 1))
        fig.subplots_adjust(bottom=0.5)
        fig.colorbar(cmap, cax=ax, orientation='horizontal', extend=None)
        return

    # 此函数可以保存图像
    def SavingFigure(self, format='jpg', dpi=600,
                     saving_directory=os.path.join(os.path.expanduser('~'),"Desktop"), file_name='untitled'):
        saving_address = saving_directory + '/' + file_name + '.' + format  # 储存地址
        plt.savefig(saving_address, dpi=dpi, format=format)
        return
