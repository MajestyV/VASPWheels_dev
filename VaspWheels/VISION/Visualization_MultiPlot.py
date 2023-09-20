# This code is written to visualize the electronic structure computed by V.A.S.P. and post-treated by VASPKIT.
# 此代码专用于可视化经过VASPKIT后处理的VASP计算结果

import matplotlib.pyplot as plt
import numpy as np
from matplotlib import colors
from matplotlib.ticker import MultipleLocator

# 额外从colors中导入颜色数据，提高代码运行效率
# 普通色值
from .colors.Custom_iColar import iColar
# 色谱
from .colormap.Custom_iColarmap import iColarmap

###############################################################################################################
# 核心绘图函数: 用于多子图组图
# 用于文章级结果图的matplotlib参数，可以作为matplotlib的全局变量载入
# num_subplot (int) 指定子图的数目; grid 指定网格的分割情况
# subplot_param指定每一幅子图的位置以及大小形状，格式为 [[(x0,y0),(w0,h0)],[(x1,y1),(w1,h1)], ...], 其中(x,y)指定位置，(w,h)指定形状
def GlobalSetting(num_subplot,grid,subplot_param,
                  figsize=(6.4,4.8),color_background='#FFFFFF',font_type='Arial',font_weight=200,**kwargs):
    fig = plt.figure(figsize=figsize)  # 设置画布大小并创建图像对象用于存放多子图

    plt.rcParams['axes.facecolor'] = color_background  # 设置画布背景颜色

    # 设置全局字体选项
    font_config = {'font.family': font_type, 'font.weight': font_weight}  # font.family设定所有字体为font_type (默认字体为Arial)
    plt.rcParams.update(font_config)  # 但是对于希腊字母(e.g. α, β, γ等)跟各种数学符号之类的不适用, Latex语法如Γ会被判断为None

    plt.rcParams.update({'xtick.direction': 'in', 'ytick.direction': 'in'})   # 设置x轴和y轴刻度线方向向内

    # 确认是否显示刻度线
    bottom_tick = kwargs['bottom_tick'] if 'bottom_tick' in kwargs else True  # 底坐标轴刻度
    top_tick = kwargs['top_tick'] if 'top_tick' in kwargs else False          # 顶坐标轴刻度
    left_tick = kwargs['left_tick'] if 'left_tick' in kwargs else True        # 左坐标轴刻度
    right_tick = kwargs['right_tick'] if 'right_tick' in kwargs else False    # 右坐标轴刻度
    plt.tick_params(bottom=bottom_tick, top=top_tick, left=left_tick, right=right_tick)

    # 设置主次刻度线
    plt.tick_params(which='major', length=5)  # 设置主刻度长度
    plt.tick_params(which='minor', length=2)  # 设置次刻度长度

    # 刻度参数
    x_major_tick = kwargs['x_major_tick'] if 'x_major_tick' in kwargs else 10                # 设置x轴主刻度标签
    y_major_tick = kwargs['y_major_tick'] if 'y_major_tick' in kwargs else 10                # 设置y轴主刻度标签
    x_minor_tick = kwargs['x_minor_tick'] if 'x_minor_tick' in kwargs else x_major_tick/5.0  # 设置x轴次刻度标签
    y_minor_tick = kwargs['y_minor_tick'] if 'y_minor_tick' in kwargs else y_major_tick/5.0  # 设置y轴次刻度标签

    # 创建各个子图对象
    subplot_list = []  # 创建一个空列表，用于存放所有子图对象
    for i in range(num_subplot):
        location, shape = subplot_param[i]  # 从子图参数中解压出当前子图的位置以及大小形状
        locals()['subplot_'+str(i+1)] = plt.subplot2grid(grid, location, colspan=shape[0], rowspan=shape[1])  # 利用内置函数动态创建变量
        subplot_list.append(locals()['subplot_'+str(i+1)])

        # 控制是否关闭坐标轴刻度
        hide_tick = kwargs['hide_tick'] if 'hide_tick' in kwargs else ''  # 控制关闭哪根坐标轴的刻度
        if hide_tick == 'x':
           locals()['subplot_'+str(i+1)].set_xticks([])  # 设置x轴刻度为空
        elif hide_tick == 'y':
           locals()['subplot_'+str(i+1)].set_yticks([])  # 设置y轴刻度为空
        elif hide_tick == 'both':
           locals()['subplot_'+str(i+1)].set_xticks([])  # 设置x轴刻度为空
           locals()['subplot_'+str(i+1)].set_yticks([])  # 设置y轴刻度为空
        else:
            # 设置主刻度
            x_major_locator = MultipleLocator(x_major_tick)  # 将x主刻度标签设置为x_major_tick的倍数
            y_major_locator = MultipleLocator(y_major_tick)  # 将y主刻度标签设置为y_major_tick的倍数
            locals()['subplot_'+str(i+1)].xaxis.set_major_locator(x_major_locator)
            locals()['subplot_'+str(i+1)].yaxis.set_major_locator(y_major_locator)
            # 设置次刻度
            x_minor_locator = MultipleLocator(x_minor_tick)  # 将x主刻度标签设置为x_major_tick/5.0的倍数
            y_minor_locator = MultipleLocator(y_minor_tick)  # 将y主刻度标签设置为y_major_tick/5.0的倍数
            locals()['subplot_'+str(i+1)].xaxis.set_minor_locator(x_minor_locator)
            locals()['subplot_'+str(i+1)].yaxis.set_minor_locator(y_minor_locator)
        # 设置刻度文本选项
        # 控制是否隐藏刻度文本的模块
        hide_ticklabel = kwargs['hide_ticklabel'] if 'hide_ticklabel' in kwargs else ''  # 控制隐藏哪根坐标轴的刻度
        if hide_ticklabel == 'x':
            locals()['subplot_'+str(i+1)].xaxis.set_ticklabels([])  # 设置x轴刻度标签为空
        elif hide_ticklabel == 'y':
            locals()['subplot_'+str(i+1)].yaxis.set_ticklabels([])  # 设置y轴刻度标签为空
        elif hide_ticklabel == 'both':
            locals()['subplot_'+str(i+1)].xaxis.set_ticklabels([])  # 设置x轴刻度标签为空
            locals()['subplot_'+str(i+1)].yaxis.set_ticklabels([])  # 设置y轴刻度标签为空
        else:
            pass

        locals()['subplot_'+str(i+1)].tick_params(which='both', colors='#BCBCBC')  # 启用这条代码以修改刻度颜色

    return subplot_list

def VisualizeScatter_Fatband(num_data,data_series,grid,subplot_param,
                             figsize=(6.4,4.8),color_background='#000080',x_major_tick=2,y_major_tick=2,
                             color_split=iColar['Gray'],colormap='jet',colormap_norm=(0,1),alpha=0.7,**kwargs):

    cmap_norm = colors.Normalize(colormap_norm[0], colormap_norm[1])  # 将色谱权重范围转化为matplotlib可读对象

    subplot_list = GlobalSetting(num_data, grid, subplot_param, figsize=figsize, color_background=color_background,
                                 y_major_tick=y_major_tick)

    for i in range(num_data):
        # 解压数据
        if len(data_series[i]) == 3:
            x, y, w = data_series[i]
            w_color, w_size = (w,w)
        elif len(data_series[i]) == 4:
            x, y, w_color, w_size = data_series[i]
        else:
            print('Please check the dimension of the data !!! ')
            return

        xlim = kwargs['xlim_list'][i] if 'xlim_list' in kwargs else (min(x),max(x))  # 设置X轴范围
        ylim = kwargs['ylim_list'][i] if 'ylim_list' in kwargs else (min(y),max(y))  # 设置Y轴范围

        subplot_list[i].scatter(x, y, s=w_size, c=w_color, cmap=colormap, norm=cmap_norm, alpha=alpha)  # 画图核心代码语句

        # 画费米面分割线
        E_fermi = kwargs['Fermi_energy'][i] if 'Fermi_energy' in kwargs else 0.0  # 费米能级位置
        subplot_list[i].hlines(E_fermi,xlim[0],xlim[1],linewidth=2, linestyles='dashed',colors=color_split, zorder=0)

        subplot_list[i].set_xlim(xlim[0], xlim[1])
        subplot_list[i].set_ylim(ylim[0], ylim[1])

        Knodes = kwargs['Knodes'] if 'Knodes' in kwargs else ('$\mathrm{K}_1$', '$\mathrm{K}_2$')
        subplot_list[i].set_xticks(xlim, Knodes, size=16)

    return