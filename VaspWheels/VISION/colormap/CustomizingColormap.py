# 此函数可以利用matplotlib自定义创建色谱（colormap），用于热度图等，需要连续变化色值的场景

import matplotlib.pyplot as plt
from matplotlib import cm, colors

# 最通用的函数，通过给定一个颜色节点列表，在颜色节点间不断插值，创建色谱
# nbins指定了颜色节点间插颜色值的数目：nbins越小，插值得到的颜色区间越少；反之，nbins越大，色谱越连续可分
def CreateColormap(color_range,nbins=100,cmap_name='untitled'):
    return cm.colors.LinearSegmentedColormap.from_list(cmap_name,color_range,nbins)  # 创建colormap

# 此函数可以通过指定起点颜色与终点颜色，创建顺序色谱
# 此处nbins指定了起点颜色与终点颜色直接插值的数目
def CreateSequentialColormap(starting_color,ending_color,nbins=100,cmap_name='untitled'):
    color_range = [starting_color,ending_color]
    return cm.colors.LinearSegmentedColormap.from_list(cmap_name,color_range,nbins)

# 此函数可以通过指定两极颜色以及中间过渡色，创建分叉色谱
# 此处的nbins指定了两个颜色极与颜色中值间的插值数目
def CreateDivergingColormap(color_pole1,color_median,color_pole2,nbins=100,cmap_name='untitled'):
    color_range = [color_pole1,color_median,color_pole2]
    return cm.colors.LinearSegmentedColormap.from_list(cmap_name,color_range,nbins)

# 此函数可生成颜色条（colorbar），以检视色谱情况
def ShowColorbar(colormap,colormap_norm,figsize=(6,1),orientation='horizontal',label='Weight'):
    cmap_norm = colors.Normalize(colormap_norm[0], colormap_norm[1])         # 将色谱范围转化为matplotlib可读对象
    plt.rcParams.update({'xtick.direction': 'in', 'ytick.direction': 'in'})  # 设置x轴和y轴刻度线方向向内
    fig, ax = plt.subplots(figsize=figsize)                                  # 创建用于绘制颜色条的画板
    fig.subplots_adjust(bottom=0.5)                                          # 调整颜色条的位置
    fig.colorbar(cm.ScalarMappable(cmap=colormap, norm=cmap_norm), cax=ax, orientation=orientation, label=label)
    return
