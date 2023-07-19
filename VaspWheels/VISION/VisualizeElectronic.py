# This code is written to visualize the electronic structure computed by V.A.S.P..

import numpy as np
import matplotlib.pyplot as plt
from .Visualization import GlobalSetting, Visualize, CustomSetting  # 从画图核心函数包直接导入画图函数，提高代码运行效率

# 额外从colors中导入颜色数据，提高代码运行效率
# 普通色值
from .colors.Custom_iColar import iColar

########################################################################################################################
# 能带可视化函数
# This function is designed for visualizing electronic bands. (此函数利用Visualization模块可视化电子能带)
def VisualizeBands(Kpath_projected,Bands,Knodes_projected,**kwargs):
    num_bands, num_kpoints = np.shape(Bands)  # 输入的能带数据Energy应该是一个num_bands行num_kpoints列的二维数组
    num_Knodes = len(Knodes_projected)        # K点路径端点的个数，即高对称点的个数

    # 一些画图参数（以动态变量的形式传入）
    title = kwargs['title'] if 'title' in kwargs else ''                                # 能带图标题，默认为无标题
    color = kwargs['color'] if 'color' in kwargs else iColar['Paris']                   # 能带曲线颜色
    color_split = kwargs['color_split'] if 'color_split' in kwargs else iColar['Gray']  # 分割线颜色
    xlim = (min(Kpath_projected), max(Kpath_projected))                                 # X轴范围
    ylim = kwargs['energy_range'] if 'energy_range' in kwargs else (-20, 20)            # Y轴范围
    ylabel = kwargs['ylabel'] if 'ylabel' in kwargs else 'Energy (eV)'                  # Y轴名称
    y_major_tick = kwargs['y_major_tick'] if 'y_major_tick' in kwargs else 2            # Y轴主刻度的步长

    # 定义好各种参数，接下来是正式的画图部分
    GlobalSetting(bottom_tick=False, y_major_tick=y_major_tick)        # 引入画图全局变量

    # 画能带图
    for i in range(num_bands):
        Visualize(Kpath_projected,Bands[i],color=color)

    # 对于能带图，有些参数Visualization模块无法设置，因此在此利用matplotlib进行修改
    # 画高对称点分割线，通过zorder=0将分割线置底
    for i in range(num_Knodes-2):  # 第一跟最后的一个高对称点跟能带图的左右边界重合，所以不必作分割线
        plt.vlines(Knodes_projected[i+1],ylim[0],ylim[1], linewidth=2, linestyles='dashed',colors=color_split,zorder=0)
    # 画费米面分割线，通过zorder=0将分割线置底
    plt.hlines(0,xlim[0],xlim[1],linewidth=2,linestyles='dashed',colors=color_split,zorder=0)

    # HighSymPath - High Symmetry Path, 高对称性点路径
    HighSymPath = kwargs['HighSymPath'] if 'HighSymPath' in kwargs else ['K'+str(n+1) for n in range(num_Knodes)]
    plt.xticks(Knodes_projected, HighSymPath, size=16)

    CustomSetting(xlim=xlim, ylim=ylim, title=title, ylabel=ylabel)  # 对能带图进行个性化设置

    return

########################################################################################################################
# 全谱分析
def FullAnalysis(Kpath_projected,Bands,Knodes_projected,DOS,Energy,**kwargs):
    num_bands, num_kpoints = np.shape(Bands)  # 输入的能带数据Energy应该是一个num_bands行num_kpoints列的二维数组
    num_Knodes = len(Knodes_projected)  # K点路径端点的个数，即高对称点的个数

    # 以动态变量的形式传入画图参数
    figsize = kwargs['figsize'] if 'figsize' in kwargs else (6, 6)                      # 图像大小
    wspace = kwargs['wspace'] if 'wspace' in kwargs else 0.0                            # 子图间的横向间隔
    hspace = kwargs['hspace'] if 'hspace' in kwargs else 0.0                            # 子图间的纵向间隔
    color = kwargs['color'] if 'color' in kwargs else iColar['Paris']                   # 曲线颜色
    color_split = kwargs['color_split'] if 'color_split' in kwargs else iColar['Gray']  # 分割线颜色
    K_range = (min(Kpath_projected), max(Kpath_projected))                              # 能带图投影K空间范围
    energy_range = kwargs['energy_range'] if 'energy_range' in kwargs else (-5, 5)      # 能带图能量值范围
    DOS_range = kwargs['DOS_range'] if 'DOS_range' in kwargs else (0, 15)               # DOS范围
    TDM_range = kwargs['TDM_range'] if 'TDM_range' in kwargs else (0, 500)              # TDM强度范围
    # K空间高对称点路径标记
    HighSymPath = kwargs['HighSymPath'] if 'HighSymPath' in kwargs else ['K' + str(n + 1) for n in range(num_Knodes)]
    bands_label = kwargs['bands_label'] if 'bands_label' in kwargs else 'Energy (eV)'   # 能带图Y轴名称
    dos_label = kwargs['dos_label'] if 'dos_label' in kwargs else 'DOS (a.u.)'          # DOS图X轴名称
    tdm_label = kwargs['tdm_label'] if 'tdm_label' in kwargs else '$\mathit{P}^2$ (a.u.)'

    # 设置画布
    # 创建图像对象，并设置坐标轴和网格配置
    fig = plt.figure(figsize=figsize)
    grid = plt.GridSpec(5, 5, wspace=wspace,hspace=hspace)

    # 设置刻度线方向
    plt.rcParams.update({'xtick.direction': 'in', 'ytick.direction': 'in'})  # 设置x轴和y轴刻度线方向向内

    # 创建子图对象
    plot_bands = fig.add_subplot(grid[1:, :4])  # 分配能带子图空间
    plot_dos = fig.add_subplot(grid[1:, 4], xticks=[], yticklabels=[])  # 分配DOS子图空间并隐藏刻度

    # 画能带子图
    for i in range(num_bands):
        plot_bands.plot(Kpath_projected, Bands[i], lw=2, color=color)
    # 画高对称点分割线
    for i in range(num_Knodes-2):  # 第一跟最后的一个高对称点跟能带图的左右边界重合，所以不必作分割线
        plot_bands.vlines(Knodes_projected[i+1],energy_range[0], energy_range[1], lw=2, ls='dashed',color=color_split)
    plot_bands.hlines(0, K_range[0], K_range[1], lw=2, ls='dashed', colors=color_split)  # 画费米面分割线
    plot_bands.set_xlim(K_range[0], K_range[1])            # 设置能带图的X轴范围
    plot_bands.set_ylim(energy_range[0], energy_range[1])  # 设置能带图的Y轴范围
    plot_bands.set_xticks(Knodes_projected, HighSymPath)   # 设置K空间高对称点为能带图的X轴标签
    plot_bands.set_ylabel(bands_label)                     # 设置能带图的Y轴名称

    # 画态密度（DOS）子图
    plot_dos.plot(DOS, Energy,lw=2, color=color)
    plot_dos.hlines(0, DOS_range[0], DOS_range[1], lw=2, ls='dashed', color=color_split)  # 画费米面分割线
    plot_dos.set_xlim(DOS_range[0], DOS_range[1])        # 设定DOS的X轴范围
    plot_dos.set_ylim(energy_range[0], energy_range[1])  # 设定DOS的Y轴范围（与能带图能量范围一致）
    plot_dos.set_xlabel(dos_label)                       # 设置DOS图的X轴名称

    # 全谱分析可选项，可视化跃迁矩阵元（Transition Dipole Moment）
    if 'TDM' in kwargs:
        TDM = kwargs['TDM']  # Transition Dipole Moment的数据
        plot_tdm = fig.add_subplot(grid[0,:4], xticks=[], xticklabels=[])  # 分配TDM子图空间并隐藏刻度
        plot_tdm.plot(Kpath_projected, TDM, linewidth=2, color=color)  # 画TDM曲线子图
        # 画高对称点分割线
        for i in range(num_Knodes - 2):  # 第一跟最后的一个高对称点跟能带图的左右边界重合，所以不必作分割线
            plot_tdm.vlines(Knodes_projected[i + 1], TDM_range[0], TDM_range[1], lw=2,ls='dashed', color=color_split)
        plot_tdm.set_xlim(K_range[0],K_range[1])      # 设置TDM的X轴范围（与能带图投影K空间范围一致）
        plot_tdm.set_ylim(TDM_range[0],TDM_range[1])  # 设置TDM图的Y轴范围
        plot_tdm.set_ylabel(tdm_label)                # 设置TDM图的X轴名称
    else:
        pass

    return







class plot_bands:
    def __init__(self):
        self.name = plot_bands



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