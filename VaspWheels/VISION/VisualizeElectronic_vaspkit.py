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