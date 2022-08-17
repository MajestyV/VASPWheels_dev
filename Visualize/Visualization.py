import numpy as np
import matplotlib.pyplot as plt
import re

class plot:
    """ This class of functions is designed to plot scientific figures in a uniform format."""
    def __init__(self):
        self.name = plot

    # 一些用于文章级结果图的matplotlib参数，可以作为matplotlib的全局变量载入
    def GlobalSetting(self,**kwargs):
        plt.rcParams['xtick.direction'] = 'in'  # 将x轴的刻度线方向设置向内
        plt.rcParams['ytick.direction'] = 'in'  # 将y轴的刻度线方向设置向内
        font_config = {'font.family': 'Times New Roman'}  # font.family设定所有字体为Times New Roman
        plt.rcParams.update(font_config)  # 但是对于希腊字母(e.g. α, β, γ等)跟各种数学符号之类的不适用, Latex语法如Γ会被判断为None
        plt.rcParams['mathtext.default'] = 'regular'  # 可以通过这个选项修改所有希腊字母以及数学符号为Times New Roman
        return

    # 这个函数可以用于画单根曲线，并确定曲线的形式，如：线型（散点还是连续曲线），线的颜色，线宽等等
    # 如有多根曲线，则可以重复调用此函数来画图
    # 这个函数的输入数据x和y必须是一维数组（也就是说(x,y)是二维数组）
    def Visulize(self,x,y,**kwargs):
        x = np.array(x)  # 将输入的数据转换为数组，以防出错
        y = np.array(y)

        # 接下来是一些曲线参数
        curve = kwargs['curve'] if 'curve' in kwargs else 'curve'  # 图谱类型参数，默认为平滑曲线图
        # 如果是图线为平滑曲线，可以通过以下列两个参数设置样式
        linestyle = kwargs['linestyle'] if 'linestyle' in kwargs else '-'  # 线型参数，默认为实线
        linewidth = kwargs['linewidth'] if 'linewidth' in kwargs else 1.0  # 控制线宽的参数
        # 如果是图线为散点图，则可以通过下列两个参数设置样式
        marker = kwargs['marker'] if 'marker' in kwargs else '.'  # 散点参数，默认为圆点
        markersize = kwargs['markersize'] if 'markersize' in kwargs else 100.0  # 散点大小参数
        color = kwargs['color'] if 'color' in kwargs else 'k'      # 颜色参数，默认为黑色

        if curve == 'scatter':  # 'scatter'字符串可以控制画散点图
            plt.scatter(x,y,marker=marker,s=markersize,color=color)
        elif curve == 'spline':  # 'spline'字符串可以控制画点线图
            plt.plot(x,y,linestyle=linestyle,linewidth=linewidth,color=color,marker=marker)
        else:
            plt.plot(x,y,linestyle=linestyle,linewidth=linewidth,color=color)

        return

    # 对于特定Figure的独特参数设置
    def FigureSetting(self,**kwargs):
        # 控制是否生成对数y轴坐标图，应注意：如果启用这个选项，所有的y轴输入都应该取正数
        log_scale = kwargs['log_scale'] if 'log_scale' in kwargs else 0
        if log_scale == 0:
            pass
        else:
            plt.yscale('log')  # y轴以对数形式计数

        # 控制图例（即legend）的模块
        legend = kwargs['legend'] if 'legend' in kwargs else 'False'  # 控制是否要图例
        location = kwargs['location'] if 'location' in kwargs else 'best'  # 若要图例，此参数可以控制图例位置
        labels = kwargs['labels'] if 'labels' in kwargs else None  # 若要图例，此参数可以设置曲线名称
        legend_size = kwargs['legend_size'] if 'legend_size' in kwargs else 14  # 控制图例大小的参数
        if legend == 'True':
            plt.legend(loc=location,labels=labels,fontsize=legend_size,frameon=False)  # 设置图例
        else:
            pass

        # 控制x轴跟y轴坐标轴名称的模块
        label_size = kwargs['label_size'] if 'label' in kwargs else 18  # 控制坐标轴名称大小的参数
        if 'xlabel' in kwargs:
            plt.xlabel(kwargs['xlabel'],fontsize=label_size)
        else:
            pass
        if 'ylabel' in kwargs:
            plt.ylabel(kwargs['ylabel'],fontsize=label_size)
        else:
            pass

        # 控制x轴跟y轴作图范围的模块，xlim跟ylim的输入必须是元组、数组或者是列表
        if 'xlim' in kwargs:
            xmin,xmax = kwargs['xlim']
            plt.xlim(xmin, xmax)
        else:
            pass
        if 'ylim' in kwargs:
            ymin,ymax = kwargs['ylim']
            plt.ylim(ymin, ymax)
        else:
            pass

        # 控制x轴跟y轴刻度大小的模块
        tick_size = kwargs['tick_size'] if 'tick_size' in kwargs else 14  # 控制x轴跟y轴刻度大小的参数
        plt.xticks(size=tick_size)
        plt.yticks(size=tick_size)

        # 控制是否隐藏刻度文本的模块
        hide_ticklabel = kwargs['hide_ticklabel'] if 'hide_ticklabel' in kwargs else ''  # 控制隐藏哪根坐标轴的刻度
        if hide_ticklabel == 'x':
            plt.xticks(color='w')  # 通过将字体变为白色（即背景的颜色）也可以起到隐藏刻度文本的作用
        elif hide_ticklabel == 'y':
            plt.yticks(color='w')
        elif hide_ticklabel == 'both':
            plt.xticks(color='w')
            plt.yticks(color='w')
        else:
            pass

        # 控制图标题的模块
        if 'title' in kwargs:
            plt.title(kwargs['title'],size=26)
        else:
            pass

        plt.tight_layout()  # 防止画图时，图像分布失衡，部分文字显示被遮挡的情况

        return

if __name__=='__main__':
    x1 = np.linspace(0,5,100)
    x2 = np.linspace(0,10,100)
    y1 = np.cos(x1)
    y2 = np.sin(x2)

    fig = plot()
    #print(np.array([x1]))

    # 应注意，唯有当x1与x2的长度一样的时候，才能把两者合成一个二维数组
    fig.Visulize(np.array([x1,x2]),np.array([y1,y2]))