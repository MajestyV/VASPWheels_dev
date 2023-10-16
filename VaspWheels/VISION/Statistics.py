import numpy as np
import scipy.stats as stats

# 此函数可以根据输入的一维数据绘制分布直方图并利用正态分布进行拟合
# https://juejin.cn/s/python%20%E6%AD%A3%E6%80%81%E5%88%86%E5%B8%83%E6%8B%9F%E5%90%88
def Histogram(figure,data,num_bins=10,dropping_extremum=True,num_dropped=1,show_fitting_param=True,**kwargs):
    # 动态参数传入
    alpha_hist = kwargs['alpha_hist'] if 'alpha_hist' in kwargs else 1.0  # 透明度，Transparency
    color_hist = kwargs['color_hist'] if 'color_hist' in kwargs else '#D68A7D'
    label_hist = kwargs['label_hist'] if 'label_hist' in kwargs else 'Untitled'
    color_fitting = kwargs['color_hist'] if 'color_hist' in kwargs else '#254E8A'
    label_fitting = kwargs['label_hist'] if 'label_hist' in kwargs else 'Untitled'
    range_fitting = kwargs['range_fitting'] if 'range_fitting' in kwargs else (min(data), max(data))  # 拟合曲线的显示范围
    npoints_fitting = kwargs['npoints_fitting'] if 'npoints_fitting' in kwargs else 100  # 拟合曲线的点数

    # 去除数据极值
    if dropping_extremum:
        i = 1
        while i <= num_dropped:
            minimum = np.argmin(data)
            maximum = np.argmax(data)
            data = np.delete(data,[minimum,maximum])
            i = i+1
    else:
        pass

    weight_list = np.ones(len(data))/len(data)  # 计算权重数组，每个片子的权重都应该是1/数据长度
    mu, sigma = stats.norm.fit(data)  # 利用scipy.stats计算数据均值以及中位数
    num_bins = num_bins  # 直方图柱子的数量

    if show_fitting_param:
        print(mu,sigma)
    else:
        pass

    # 直方图函数，x为x轴的值，normed=1表示为概率密度，即和为一，绿色方块，色深参数0.5.返回n个概率，直方块左边线的x值，及各个方块对象
    n, bins, patches = figure.hist(data, num_bins, weights=weight_list, alpha=alpha_hist, color=color_hist, label=label_hist)
    print(n,bins,patches)
    # 画拟合曲线
    x_fitting = np.linspace(range_fitting[0],range_fitting[1],npoints_fitting)
    y_fitting = stats.norm.pdf(x_fitting,mu,sigma)  # 拟合一条最佳正态分布曲线y
    figure.plot(x_fitting, y_fitting, color=color_fitting, linestyle='--',label=label_fitting,linewidth=2)  # 绘制拟合曲线

    return