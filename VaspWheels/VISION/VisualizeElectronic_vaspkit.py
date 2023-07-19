# This code is written to visualize the electronic structure computed by V.A.S.P. and post-treated by VASPKIT.
# 此代码专用于可视化经过VASPKIT后处理的VASP计算结果

import numpy as np
import matplotlib.pyplot as plt
from matplotlib import colors
from .Visualization import GlobalSetting, CustomSetting  # 从画图核心函数包直接导入画图函数，提高代码运行效率

# 额外从colors中导入颜色数据，提高代码运行效率
# 普通色值
from .colors.Custom_iColar import iColar
# 色谱
from .colormap.Custom_iColarmap import iColarmap

########################################################################################################################
# 能带可视化模块

# 能带可视化函数
# This function is designed for visualizing electronic bands. (此函数利用Visualization模块可视化电子能带)
def VisualizeBands(x_band,y_band,Knodes_projected,**kwargs):
    # 一些画图参数（以动态变量的形式传入）
    title = kwargs['title'] if 'title' in kwargs else ''                                # 能带图标题，默认为无标题
    color = kwargs['color'] if 'color' in kwargs else iColar['Paris']                   # 能带曲线颜色
    color_split = kwargs['color_split'] if 'color_split' in kwargs else iColar['Gray']  # 分割线颜色
    xlim = (np.min(x_band), np.max(x_band))                                 # X轴范围
    ylim = kwargs['energy_range'] if 'energy_range' in kwargs else (-5, 5)            # Y轴范围
    ylabel = kwargs['ylabel'] if 'ylabel' in kwargs else 'Energy (eV)'                  # Y轴名称
    y_major_tick = kwargs['y_major_tick'] if 'y_major_tick' in kwargs else 2            # Y轴主刻度的步长

    # 定义好各种参数，接下来是正式的画图部分
    GlobalSetting(bottom_tick=False, y_major_tick=y_major_tick)        # 引入画图全局变量

    # 画能带图
    plt.plot(x_band,y_band,c=color,linewidth=2)

    # 对于能带图，有些参数Visualization模块无法设置，因此在此利用matplotlib进行修改
    # 画高对称点分割线，通过zorder=0将分割线置底
    num_Knodes = len(Knodes_projected)  # K点路径端点的个数，即高对称点的个数
    for i in range(num_Knodes-2):  # 第一跟最后的一个高对称点跟能带图的左右边界重合，所以不必作分割线
        plt.vlines(Knodes_projected[i+1],ylim[0],ylim[1], linewidth=2, linestyles='dashed',colors=color_split,zorder=0)
    # 画费米面分割线，通过zorder=0将分割线置底
    plt.hlines(0,xlim[0],xlim[1],linewidth=2,linestyles='dashed',colors=color_split,zorder=0)

    # HighSymPath - High Symmetry Path, 高对称性点路径
    HighSymPath = kwargs['HighSymPath'] if 'HighSymPath' in kwargs else ['K'+str(n+1) for n in range(num_Knodes)]
    plt.xticks(Knodes_projected, HighSymPath, size=16)

    CustomSetting(xlim=xlim, ylim=ylim, title=title, ylabel=ylabel)  # 对能带图进行个性化设置

    return

# 投影能带可视化函数
# This function is designed for visualizing electronic bands. (此函数利用Visualization模块可视化电子能带)
def VisualizeProjectedBands(x_band, y_band, w_band, Knodes_projected, **kwargs):
    # 一些画图参数（以动态变量的形式传入）
    title = kwargs['title'] if 'title' in kwargs else ''  # 能带图标题，默认为无标题
    colormap = kwargs['colormap'] if 'colormap' in kwargs else iColarmap['Coolwarm']              # colormap，色谱
    color_split = kwargs['color_split'] if 'color_split' in kwargs else iColar['Gray']            # 分割线颜色
    color_background = kwargs['color_background'] if 'color_background' in kwargs else '#FFFFFF'  # 背景颜色
    xlim = (np.min(x_band), np.max(x_band))                                                       # X轴范围
    ylim = kwargs['energy_range'] if 'energy_range' in kwargs else (-5, 5)                        # Y轴范围
    ylabel = kwargs['ylabel'] if 'ylabel' in kwargs else 'Energy (eV)'                            # Y轴名称
    y_major_tick = kwargs['y_major_tick'] if 'y_major_tick' in kwargs else 2                      # Y轴主刻度的步长
    size_band = kwargs['size_band'] if 'size_band' in kwargs else 2                               # 能带散点的尺寸（若输入二维数据，可画fatband）

    # 设置色谱的对应的权重范围
    if 'colormap_norm' in kwargs:
        colormap_norm = kwargs['colormap_norm']
    else:
        colormap_norm = (np.min(w_band), np.max(w_band))  # 默认为权重的最小值到最大值
    cmap_norm = colors.Normalize(colormap_norm[0],colormap_norm[1])  # 将色谱范围转化为matplotlib可读对象

    # 定义好各种参数，接下来是正式的画图部分
    plt.rcParams['axes.facecolor'] = color_background  # 更换背景颜色
    GlobalSetting(bottom_tick=False, y_major_tick=y_major_tick)  # 引入画图全局变量

    # 画投影能带（形式可参考：https://blog.shishiruqi.com//2019/05/19/pymatgen-band/）
    # 用Matplotlib绘制渐变的彩色曲线：https://blog.csdn.net/xufive/article/details/127492212
    # 利用散点图实现渐变：https://www.brothereye.cn/python/427/
    plt.scatter(x_band, y_band, s=size_band, c=w_band, cmap=colormap, norm=cmap_norm)

    # 画高对称点分割线
    num_Knodes = len(Knodes_projected)  # K点路径端点的个数，即高对称点的个数
    num_segments = num_Knodes - 1  # 能带分段数，为K点路径端点数减一
    for i in range(1, num_segments):  # 第一跟最后的一个高对称点跟能带图的左右边界重合，所以不必作分割线
        plt.vlines(Knodes_projected[i], ylim[0], ylim[1], linewidth=2, linestyles='dashed', colors=color_split, zorder=0)
    # 画费米面分割线
    plt.hlines(0, xlim[0], xlim[1], linewidth=2, linestyles='dashed', colors=color_split, zorder=0)

    # HighSymPath - High Symmetry Path, 高对称性点路径
    HighSymPath = kwargs['HighSymPath'] if 'HighSymPath' in kwargs else ['K'+str(n+1) for n in range(num_Knodes)]
    plt.xticks(Knodes_projected, HighSymPath, size=16)

    CustomSetting(xlim=xlim, ylim=ylim, title=title, ylabel=ylabel)  # 对能带图进行个性化设置

    return

########################################################################################################################
# 态密度（DOS）可视化模块

# DOS可视化函数
def VisualizeDOS(x_DOS, y_DOS, mode='single', **kwargs):
    # 一些画图参数（以动态变量的形式传入）
    title = kwargs['title'] if 'title' in kwargs else ''                                     # 能带图标题，默认为无标题
    figsize = kwargs['figsize'] if 'figsize' in kwargs else (2.1, 4.8)                           # 图像大小
    color = kwargs['color'] if 'color' in kwargs else iColar['Paris']                        # 能带曲线颜色
    color_split = kwargs['color_split'] if 'color_split' in kwargs else iColar['Gray']       # 分割线颜色
    xlim = kwargs['dos_range'] if 'dos_range' in kwargs else (np.min(x_DOS), np.max(x_DOS))  # X轴范围
    ylim = kwargs['energy_range'] if 'energy_range' in kwargs else (-5, 5)                   # Y轴范围
    xlabel = kwargs['xlabel'] if 'xlabel' in kwargs else 'DOS (a.u.)'                        # X轴名称
    ylabel = kwargs['ylabel'] if 'ylabel' in kwargs else 'Energy (eV)'                       # Y轴名称
    y_major_tick = kwargs['y_major_tick'] if 'y_major_tick' in kwargs else 2                 # Y轴主刻度的步长

    GlobalSetting(figsize=figsize,bottom_tick=False,y_major_tick=y_major_tick)

    if mode == 'single':
        plt.plot(x_DOS,y_DOS,c=color,linewidth=2)
    elif mode == 'multiple':  # 可视化多条DOS曲线的模式
        num_dos = int(len(x_DOS))  # 要可视化的DOS数目
        color_list = kwargs['color_list'] if 'color_list' in kwargs else [color]*num_dos
        for i in range(num_dos):
            plt.plot(x_DOS[i],y_DOS[i],c=color_list[i],linewidth=2)
    else:
        print('Please specify visualization mode: "single" or "multiple" ?')
        return

    plt.hlines(0,xlim[0],xlim[1], linewidth=2, linestyles='dashed', colors=color_split, zorder=0)  # 画费米面分割线

    CustomSetting(xlim=xlim, ylim=ylim, title=title, xlabel=xlabel, ylabel=ylabel)  # 对DOS图进行个性化设置

    return

########################################################################################################################
# 全谱分析
def FullAnalysis(x_band,y_band,Knodes_projected,x_DOS,y_DOS,**kwargs):
    # 以动态变量的形式传入画图参数
    figsize = kwargs['figsize'] if 'figsize' in kwargs else (6, 6)                                # 图像大小
    wspace = kwargs['wspace'] if 'wspace' in kwargs else 0.0                                      # 子图间的横向间隔
    hspace = kwargs['hspace'] if 'hspace' in kwargs else 0.0                                      # 子图间的纵向间隔
    color = kwargs['color'] if 'color' in kwargs else iColar['Paris']                             # 曲线颜色
    color_split = kwargs['color_split'] if 'color_split' in kwargs else iColar['Gray']            # 分割线颜色
    K_range = (min(x_band), max(x_band))                                                          # 能带图投影K空间范围
    energy_range = kwargs['energy_range'] if 'energy_range' in kwargs else (-5, 5)                # 能带图能量值范围
    DOS_range = kwargs['dos_range'] if 'dos_range' in kwargs else (np.min(x_DOS), np.max(x_DOS))  # DOS范围
    bands_label = kwargs['bands_label'] if 'bands_label' in kwargs else 'Energy (eV)'             # 能带图Y轴名称
    dos_label = kwargs['dos_label'] if 'dos_label' in kwargs else 'DOS (a.u.)'                    # DOS图X轴名称

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
    plot_bands.plot(x_band, y_band, lw=2, color=color)
    # 画高对称点分割线
    num_Knodes = len(Knodes_projected)  # K点路径端点的个数，即高对称点的个数
    HighSymPath = kwargs['HighSymPath'] if 'HighSymPath' in kwargs else ['K' + str(n + 1) for n in range(num_Knodes)]  # K空间高对称点路径标记
    for i in range(num_Knodes-2):  # 第一跟最后的一个高对称点跟能带图的左右边界重合，所以不必作分割线
        plot_bands.vlines(Knodes_projected[i+1],energy_range[0], energy_range[1], lw=2, ls='dashed',color=color_split,zorder=0)
    plot_bands.hlines(0, K_range[0], K_range[1], lw=2, ls='dashed', colors=color_split,zorder=0)  # 画费米面分割线
    plot_bands.set_xlim(K_range[0], K_range[1])            # 设置能带图的X轴范围
    plot_bands.set_ylim(energy_range[0], energy_range[1])  # 设置能带图的Y轴范围
    plot_bands.set_xticks(Knodes_projected, HighSymPath)   # 设置K空间高对称点为能带图的X轴标签
    plot_bands.set_ylabel(bands_label)                     # 设置能带图的Y轴名称

    # 画态密度（DOS）子图
    plot_dos.plot(x_DOS, y_DOS, lw=2, color=color)
    plot_dos.hlines(0, DOS_range[0], DOS_range[1], lw=2, ls='dashed', color=color_split, zorder=0)  # 画费米面分割线
    plot_dos.set_xlim(DOS_range[0], DOS_range[1])        # 设定DOS的X轴范围
    plot_dos.set_ylim(energy_range[0], energy_range[1])  # 设定DOS的Y轴范围（与能带图能量范围一致）
    plot_dos.set_xlabel(dos_label)                       # 设置DOS图的X轴名称

    # 全谱分析可选项，可视化跃迁矩阵元（Transition Dipole Moment）
    if 'TDM' in kwargs:
        x_TDM, y_TDM = kwargs['TDM']  # Transition Dipole Moment的数据
        TDM_range = kwargs['TDM_range'] if 'TDM_range' in kwargs else (np.min(y_DOS), np.max(y_DOS))  # TDM强度范围
        tdm_label = kwargs['tdm_label'] if 'tdm_label' in kwargs else '$\mathit{P}^2$ (a.u.)'

        plot_tdm = fig.add_subplot(grid[0,:4], xticks=[], xticklabels=[])  # 分配TDM子图空间并隐藏刻度
        plot_tdm.plot(x_TDM, y_TDM, linewidth=2, color=color)  # 画TDM曲线子图
        # 画高对称点分割线
        for i in range(num_Knodes - 2):  # 第一跟最后的一个高对称点跟能带图的左右边界重合，所以不必作分割线
            plot_tdm.vlines(Knodes_projected[i+1],TDM_range[0],TDM_range[1],lw=2,ls='dashed',color=color_split,zorder=0)
        plot_tdm.set_xlim(K_range[0],K_range[1])      # 设置TDM的X轴范围（与能带图投影K空间范围一致）
        plot_tdm.set_ylim(TDM_range[0],TDM_range[1])  # 设置TDM图的Y轴范围
        plot_tdm.set_ylabel(tdm_label)                # 设置TDM图的X轴名称
    else:
        pass

    return