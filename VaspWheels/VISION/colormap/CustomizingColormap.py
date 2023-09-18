# 此函数可以利用matplotlib自定义创建色谱（colormap），用于热度图等，需要连续变化色值的场景

import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.colors import Normalize,ListedColormap, LinearSegmentedColormap

##########################################################
# Abbreviation:                                          #
# cmap - colormap，色谱                                   #
# nbins - number of bins，指定了颜色节点间插颜色值的数目       #
##########################################################

########################################################################################################################
# 基于matplotlib内置色谱创建新色谱模块

# 从matplotlib已有色谱中获取特定颜色值，返回的颜色值为归一化的RGB色
# cmap_name是目标色谱的名字，color_index指明了要获取的颜色序号，nbins指明了要将色谱分割成多少份（即指定颜色起点跟终点间插颜色值的数目）
def GetColor_from_Colormap(cmap,color_index,nbins=256):
    cmap = cm.get_cmap(cmap, nbins)  # 利用get_cmap()函数提取matplotlib内置色谱，返回值是matplotlib可读对象
    return cmap(color_index)

# 从matplotlib内置的色谱中截取目标色谱
def InterceptMatplotlibColormap(cmap_name,range,nbins=256):
    cmap = cm.get_cmap(cmap_name,nbins)       # 利用get_cmap()函数提取matplotlib内置色谱，返回值是matplotlib可读对象
    cmap_list = cmap(np.linspace(0,1,nbins))  # 将cmap转换成列表，这样子才能用ListedColormap函数重新生成色谱
    cmap_intercepted = ListedColormap(cmap_list[range[0]:range[1]])
    return cmap_intercepted

########################################################################################################################
# 自定义色谱创建模块

# 最通用的函数，通过给定一个颜色节点列表，在颜色节点间不断插值，创建色谱
# nbins指定了颜色节点间插颜色值的数目：nbins越小，插值得到的颜色区间越少；反之，nbins越大，色谱越连续可分
def CreateColormap(color_range,nbins=256,cmap_name='untitled'):
    return LinearSegmentedColormap.from_list(cmap_name,color_range,nbins)  # 创建colormap

# 此函数可以通过指定起点颜色与终点颜色，创建顺序色谱
# 此处nbins指定了起点颜色与终点颜色直接插值的数目
def CreateSequentialColormap(starting_color,ending_color,nbins=256,cmap_name='untitled'):
    color_range = [starting_color,ending_color]
    return LinearSegmentedColormap.from_list(cmap_name,color_range,nbins)

# 此函数可以通过指定两极颜色以及中间过渡色，创建分叉色谱
# 此处的nbins指定了两个颜色极与颜色中值间的插值数目
def CreateDivergingColormap(color_pole1,color_median,color_pole2,nbins=256,cmap_name='untitled'):
    color_range = [color_pole1,color_median,color_pole2]
    return LinearSegmentedColormap.from_list(cmap_name,color_range,nbins)

# 此函数可生成颜色条（colorbar），以检视色谱情况
def ShowColorbar(colormap,colormap_norm,figsize=(6,1),orientation='horizontal',label='Weight'):
    cmap_norm = Normalize(colormap_norm[0], colormap_norm[1])         # 将色谱范围转化为matplotlib可读对象
    plt.rcParams.update({'xtick.direction': 'in', 'ytick.direction': 'in'})  # 设置x轴和y轴刻度线方向向内
    fig, ax = plt.subplots(figsize=figsize)                                  # 创建用于绘制颜色条的画板
    fig.subplots_adjust(bottom=0.5)                                          # 调整颜色条的位置
    fig.colorbar(cm.ScalarMappable(cmap=colormap, norm=cmap_norm), cax=ax, orientation=orientation, label=label)
    return
