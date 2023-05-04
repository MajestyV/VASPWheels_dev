# This code is written to visualize band structures, both electronic or vibrational.
# Specialized for handling calculation results gained from V.A.S.P. and Phonopy.

import numpy as np
import matplotlib.pyplot as plt
# from Gallery.colors import crayons, xkcd_rgb
from .Gallery import crayons, xkcd_rgb
from VaspWheels import Visualization

####################################################################################################################
VI = Visualization.plot()  # 调用Visualization模块
#####################################################################################################################

class plot_bands:
    def __init__(self):
        self.name = plot_bands

    #################################################################################################################
    # 能带可视化模块
    # This function is designed for visualizing electronic bands. (此函数利用Visualization模块可视化电子能带)
    def Electron_bands(self,Kpath_projected,Bands,Knodes_projected,**kwargs):
        num_bands, num_kpoints = np.shape(Bands)  # 输入的能带数据Energy应该是一个num_bands行num_kpoints列的二维数组
        num_Knodes = len(Knodes_projected)         # K点路径端点的个数，即高对称点的个数

        # 一些画图参数（以动态变量的形式传入）
        title = kwargs['title'] if 'title' in kwargs else ''  # 能带图标题，默认为无标题
        # color = kwargs['color'] if 'color' in kwargs else np.array([70,148,203])/255.0                     # 能带曲线颜色
        # color = kwargs['color'] if 'color' in kwargs else VI.MorandiColor('Paris')  # 能带曲线颜色
        color = kwargs['color'] if 'color' in kwargs else crayons['Navy Blue']  # 能带曲线颜色
        color_split = kwargs['color_split'] if 'color_split' in kwargs else VI.MorandiColor('Grey')  # 分割线颜色
        xlim = (min(Kpath_projected), max(Kpath_projected))       # X轴范围
        ylim = kwargs['ylim'] if 'ylim' in kwargs else (-20, 20)  # Y轴范围
        ylabel = kwargs['ylabel'] if 'ylabel' in kwargs else 'Energy (eV)'        # y轴名称
        y_major_tick = kwargs['y_major_tick'] if 'y_major_tick' in kwargs else 2  # y轴主刻度的步长

        # 定义好各种参数，接下来是正式的画图部分
        VI.GlobalSetting(bottom_tick=False, y_major_tick=y_major_tick)  # 引入画图全局变量

        # 画能带图
        for i in range(num_bands):
            VI.Visualize(Kpath_projected,Bands[i],color=color)

        # 对于能带图，有些参数Visualization模块无法设置，因此在此利用matplotlib进行修改
        # 画高对称点分割线
        for i in range(num_Knodes-2):  # 第一跟最后的一个高对称点跟能带图的左右边界重合，所以不必作分割线
            plt.vlines(Knodes_projected[i+1],ylim[0],ylim[1], linewidth=2, linestyles='dashed',colors=color_split)
        # 画费米面分割线
        plt.hlines(0,xlim[0],xlim[1],linewidth=2,linestyles='dashed',colors=color_split)

        # HighSymPoint - High Symmetry Point, 高对称性点
        HighSymPoint = kwargs['HighSymPoint'] if 'HighSymPoint' in kwargs else ['K'+str(n+1) for n in range(num_Knodes)]
        plt.xticks(Knodes_projected, HighSymPoint, size=16)

        # 利用Visualization模块内置函数对能带图细节进行修改
        VI.FigureSetting(xlim=xlim, ylim=ylim, title=title, ylabel=ylabel)

        return

    # This function is designed for visualizing phonon bands. (此函数利用Visualization模块可视化声子能带)
    def Phonon_bands(self, Kpath_projected, Frequency, Knodes_projected, **kwargs):
        return

    def VisualizePhononBand(self,band_yaml,degree_of_freedom=3,**kwargs):
        raw_data = self.ReadPhonopyData(band_yaml)
        q_projected, frequency, nbands, nqpoint, npath = self.RearrangePhonopyData(raw_data,degree_of_freedom)

        # HSP - High Symmetry Point
        HSP_notation = kwargs['Kpoints'] if 'Kpoints' in kwargs else ['P' + str(n + 1) for n in range(npath+1)]
        HSP_position = [q_projected[0]]+[q_projected[int(nqpoint/npath)*i-1] for i in range(1,npath)]+[q_projected[len(q_projected)-1]]
        # 把初始点跟终点都包括进去

        xmin = q_projected[0]  # X轴范围
        xmax = q_projected[len(q_projected) - 1]
        ylim = kwargs['ylim'] if 'ylim' in kwargs else [0, 15]  # Y轴范围
        ymin, ymax = ylim
        color = kwargs['color'] if 'color' in kwargs else 'k'
        label = kwargs['label'] if 'label' in kwargs else None
        linewidth = kwargs['linewidth'] if 'linewidth' in kwargs else '0.6'

        label_band = kwargs['label_band'] if 'label_band' in kwargs else 'False'
        bands_labelled = kwargs['bands_labelled'] if 'bands_labelled' in kwargs else None
        labelling_color = kwargs['labelling_color'] if 'labelling_color' in kwargs else 'r'

        # 单位转换(太赫兹到波数)：1 THz= 33.35641 cm-1
        unit = kwargs['unit'] if 'unit' in kwargs else 'THz'
        if unit == 'cm-1':
            frequency = [[frequency[i][j]*33.35641 for j in range(len(frequency[i]))] for i in range(len(frequency))]
        else:
            pass

        for n in range(nbands):
            if label_band == 'True':
                if n+1 in bands_labelled:
                    #if bands_labelled.index(n+1) == 0:
                        #plt.plot(q_projected, frequency[n], linewidth=linewidth, color=labelling_color, label='Raman active')
                    #else:
                        #plt.plot(q_projected, frequency[n], linewidth=linewidth, color=labelling_color)
                    plt.plot(q_projected, frequency[n], linewidth=linewidth, color=labelling_color)
                else:
                    plt.plot(q_projected, frequency[n], linewidth=linewidth, color=color)
            else:
                if label and n==0:
                    plt.plot(q_projected,frequency[n],linewidth=linewidth,color=color,label=label)
                else:
                    plt.plot(q_projected,frequency[n],linewidth=linewidth,color=color)
        plt.xlim(xmin,xmax)
        plt.ylim(ymin,ymax)

        plt.vlines(HSP_position,ymin,ymax,linewidth=0.5,linestyles='dashed',colors='k')
        plt.hlines(0,xmin,xmax,linewidth=0.5,linestyles='dashed',colors='k')

        plt.xticks(HSP_position, HSP_notation, size=20)
        plt.yticks(size=14)

        if unit == 'cm-1':
            plt.ylabel('$\omega$ ($cm^{-1}$)', size=18)
        else:
            plt.ylabel('Frequency (THz)', size=18)

        if 'title' in kwargs:
            plt.title(kwargs['title'],size=26)
        else:
            pass

        return HSP_position, HSP_notation

if __name__=='__main__':
    EIGENVAL = 'D:/MaterialsGallery/Testing/MoS2_monolayer_test/result_double_cell/EIGENVAL'
    plot = Plotting()
    #Kpoints = [r'$\Gamma$','M', 'K', r'$\Gamma$', 'A', 'L', 'H', 'A']
    #path = [[0, 0, 0], [0.5, 0, 0], [1.0 / 3.0, 1.0 / 3.0, 0], [0, 0, 0], [0,0,1/2.0], [1/2.0,0,1/2.0], [1/3.0, 1/3.0, 1/2.0], [0,0,1/2.0]]
    Kpoints = [r'$\Gamma$', 'M', 'K', r'$\Gamma$']
    path = [[0, 0, 0], [0.5, 0, 0], [1.0 / 3.0, 1.0 / 3.0, 0], [0, 0, 0]]
    lattice = ['HEX', [3.16, 3.16, 12.9, 90, 90, 120], 'primitive']
    a = plot.Ebands(EIGENVAL,path,LatticeCorrection='True',Lattice=lattice,ShiftFermi='False',Efermi=6.685,Kpoints=Kpoints,ylim=(-5,5),title='Band structure of 7-layer MoS2',latex='False')
    #print(len(a['energy'][0]))
    #print(len(a['occupation'][31]))
    # print(a[1])
    #kpath.GetKpath(saving_directory,path,59)