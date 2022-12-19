import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator, FormatStrFormatter
from mpl_toolkits.mplot3d import Axes3D
from os import path

class plot:
    """ This class of functions is designed to plot scientific figures in a uniform format."""
    def __init__(self):
        self.name = plot
        self.default_directory = path.dirname(__file__) + '/'  # 设置这个代码文件所在的文件夹为默认读写目录

    ###############################################################################################################
    # 颜色模块
    # RGB值转换函数
    def RGB(self,r,g,b): return np.array([r,g,b])/255.0  # 将RGB值归一化的函数，只有归一化的RGB值才能被matplotlib读取

    # 此函数可以转换CMYK色值到RGB色值
    def CMYK_to_RGB(self,c, m, y, k, cmyk_scale=100, rgb_scale=255):
        r = rgb_scale * (1.0 - c / float(cmyk_scale)) * (1.0 - k / float(cmyk_scale))
        g = rgb_scale * (1.0 - m / float(cmyk_scale)) * (1.0 - k / float(cmyk_scale))
        b = rgb_scale * (1.0 - y / float(cmyk_scale)) * (1.0 - k / float(cmyk_scale))
        return np.array([r, g, b])/255.0

    # 常用配色
    def Color(self,mode):
        color_dict = {
                      'Black_n_Red': [self.RGB(7,7,7),self.RGB(255,59,59)],
                      'Red_n_Black': [self.RGB(255,59,59),self.RGB(7,7,7)],
                      'Blue_n_Grey': [self.RGB(57, 83, 163),self.RGB(92,92,92)],
                      'Three_contrast_OldFashion': [self.RGB(7, 7, 7), self.RGB(57, 83, 163), self.RGB(255, 59, 59)],
                      'Red_n_Blue': [self.RGB(239,76,77),self.RGB(70,148,203)],
                      'Red_n_Grey': [self.RGB(239,76,77),self.RGB(92,92,92)],
                      'Three_contrast': [self.RGB(7,7,7),self.RGB(57,83,163),self.RGB(239,76,77)],
                      'One_color': [self.RGB(7,7,7)],
                      'Two_color': [self.RGB(254,129,125),self.RGB(129,184,223)],
                      'Three_color': [self.RGB(77,133,189),self.RGB(247,144,61),self.RGB(89,169,90)],
                      'Four_color': [self.RGB(23,23,23),self.RGB(6,223,6),self.RGB(255,28,0),self.RGB(0,37,255)],
                      'Five_color': [self.RGB(1,86,153),self.RGB(250,192,15),self.RGB(243,118,74),
                                     self.RGB(95,198,201),self.RGB(79,89,109)]
                      }
        return color_dict[mode]

    # 莫兰迪色系
    def MorandiColor(self,mode,**kwargs):
        c, m, y, k =  kwargs['cmyk'] if 'cmyk' in kwargs else (1,1,1,1)      # 测试色值，通过输入这个值可以方便地测试新颜色的效果
        c1,m1,y1,k1 = kwargs['custom'] if 'custom' in kwargs else (1,1,1,1)  # 自定义色值，通过这个值可以输入自定义颜色

        color_dict = {
                      'Testing':    self.CMYK_to_RGB(c,m,y,k),
                      'Custom':     self.CMYK_to_RGB(c1,m1,y1,k1),
                      'Black':      self.CMYK_to_RGB(80,72,69,36),
                      'Pinkgrey':   self.CMYK_to_RGB(0,10,10,30),
                      'Grey':       self.CMYK_to_RGB(0,0,0,54),
                      'Lightgrey':  self.CMYK_to_RGB(0,0,0,33),
                      'Deepgrey':   self.CMYK_to_RGB(0,0,0,73),
                      'Darkgrey':   self.CMYK_to_RGB(0,0,0,83),
                      'Orangered':  self.CMYK_to_RGB(0,81,81,30),
                      'Redred':     self.CMYK_to_RGB(0,90,90,10),
                      'Red':        self.CMYK_to_RGB(0,75,75,35),
                      'Wine':       self.CMYK_to_RGB(0,69,51,42),
                      'Green':      self.CMYK_to_RGB(67,50,62,0),
                      'Spring':     self.CMYK_to_RGB(32,22,27,0),
                      'Forrest':    self.CMYK_to_RGB(87,70,82,0),
                      'Blue':       self.CMYK_to_RGB(78,65,44,3),
                      'Lightblue':  self.CMYK_to_RGB(30,20,8,8),
                      'Deepblue':   self.CMYK_to_RGB(86,73,46,8),
                      'Paris':      self.CMYK_to_RGB(80,70,48,8),
                      'Magicblue':  self.CMYK_to_RGB(43,19,0,13),
                      'Purpleblue': self.CMYK_to_RGB(40,30,8,8),
                      'Red_n_Black': (self.CMYK_to_RGB(0,90,90,10),self.CMYK_to_RGB(80,72,69,36)),
                      'Five_color': (self.CMYK_to_RGB(0,32,38,38),self.CMYK_to_RGB(0,22,31,25),
                                     self.CMYK_to_RGB(16,28,0,22),self.CMYK_to_RGB(0,26,28,12),
                                     self.CMYK_to_RGB(6,21,0,51)),
                      'Colormap_grey':   (self.CMYK_to_RGB(0,0,0,33),self.CMYK_to_RGB(0,0,0,83)),
                      'Colormap_red':    (self.CMYK_to_RGB(0,10,10,30),self.CMYK_to_RGB(0,81,81,30)),
                      'Colormap_green':  (self.CMYK_to_RGB(32,22,27,0),self.CMYK_to_RGB(87,70,82,0)),
                      'Colormap_blue':   (self.CMYK_to_RGB(30,20,8,8),self.CMYK_to_RGB(80,70,48,8))
                      }

        return color_dict[mode]

    ###############################################################################################################
    # 快速可视化分析模块
    # 此函数可以对数据进行三维可视化
    def Visualize3D(self,x,y,z,**kwargs):
        # 定义图像和三维坐标轴
        fig = plt.figure()
        ax = Axes3D(fig)  # 也可以使用：ax = plt.axes(projection='3d')

        mode = kwargs['mode'] if 'mode' in kwargs else 'curve'  # 画图模式，默认为曲线
        if mode == 'curve':
            ax.plot3D(x, y, z)
        elif mode == 'surface':
            ax.plot_surface(x, y, z)
        elif mode == 'scatter':
            ax.scatter(x,y,z)
        else:
            pass

        return

    # 此函数可以将三维数据投影成等高线图，适用于多种场景如：势能（能量）面分析，误差最小化等
    def Visualiza_contour(self):
        return

    ###############################################################################################################
    # 精细画图模块
    # 一些用于文章级结果图的matplotlib参数，可以作为matplotlib的全局变量载入
    def GlobalSetting(self,**kwargs):
        # 设置刻度线方向
        plt.rcParams['xtick.direction'] = 'in'  # 将x轴的刻度线方向设置向内
        plt.rcParams['ytick.direction'] = 'in'  # 将y轴的刻度线方向设置向内

        # 确认是否显示刻度线
        bottom_tick = kwargs['bottom_tick'] if 'bottom_tick' in kwargs else True  # 底坐标轴刻度
        top_tick = kwargs['top_tick'] if 'top_tick' in kwargs else False          # 顶坐标轴刻度
        left_tick = kwargs['left_tick'] if 'left_tick' in kwargs else True    # 左坐标轴刻度
        right_tick = kwargs['right_tick'] if 'right_tick' in kwargs else False        # 右坐标轴刻度
        plt.tick_params(bottom=bottom_tick, top=top_tick, left=left_tick, right=right_tick)

        # 设置主次刻度线
        plt.tick_params(which='major', length=5)  # 设置主刻度长度
        plt.tick_params(which='minor', length=2)  # 设置次刻度长度

        if 'figsize' in kwargs:
            plt.figure(figsize=kwargs['figsize'])
        else:
            pass

        # 创建图例对象
        ax = plt.subplot(111)  # 注意有些参数（比如刻度）一般都在ax中设置,不在plot中设置

        # 刻度参数
        x_major_tick = kwargs['x_major_tick'] if 'x_major_tick' in kwargs else 10  # 设置x轴主刻度标签
        y_major_tick = kwargs['y_major_tick'] if 'y_major_tick' in kwargs else 10  # 设置y轴主刻度标签
        x_minor_tick = kwargs['x_minor_tick'] if 'x_minor_tick' in kwargs else x_major_tick / 5.0  # 设置x轴次刻度标签
        y_minor_tick = kwargs['y_minor_tick'] if 'y_minor_tick' in kwargs else y_major_tick / 5.0  # 设置y轴次刻度标签

        # 控制是否关闭坐标轴刻度
        hide_tick = kwargs['hide_tick'] if 'hide_tick' in kwargs else ''  # 控制关闭哪根坐标轴的刻度
        if hide_tick == 'x':
            ax.set_xticks([])  # 设置x轴刻度为空
        elif hide_tick == 'y':
            ax.set_yticks([])  # 设置y轴刻度为空
        elif hide_tick == 'both':
            ax.set_xticks([])  # 设置x轴刻度为空
            ax.set_yticks([])  # 设置y轴刻度为空
        else:
            # 设置主刻度
            x_major_locator = MultipleLocator(x_major_tick)  # 将x主刻度标签设置为x_major_tick的倍数
            y_major_locator = MultipleLocator(y_major_tick)  # 将y主刻度标签设置为y_major_tick的倍数
            ax.xaxis.set_major_locator(x_major_locator)
            ax.yaxis.set_major_locator(y_major_locator)
            # 设置次刻度
            x_minor_locator = MultipleLocator(x_minor_tick)  # 将x主刻度标签设置为x_major_tick/5.0的倍数
            y_minor_locator = MultipleLocator(y_minor_tick)  # 将y主刻度标签设置为y_major_tick/5.0的倍数
            ax.xaxis.set_minor_locator(x_minor_locator)
            ax.yaxis.set_minor_locator(y_minor_locator)
        # 设置刻度文本选项
        # 控制是否隐藏刻度文本的模块
        hide_ticklabel = kwargs['hide_ticklabel'] if 'hide_ticklabel' in kwargs else ''  # 控制隐藏哪根坐标轴的刻度
        if hide_ticklabel == 'x':
            ax.xaxis.set_ticklabels([])  # 设置x轴刻度标签为空
        elif hide_ticklabel == 'y':
            ax.yaxis.set_ticklabels([])  # 设置y轴刻度标签为空
        elif hide_ticklabel == 'both':
            ax.xaxis.set_ticklabels([])  # 设置x轴刻度标签为空
            ax.yaxis.set_ticklabels([])  # 设置y轴刻度标签为空
        else:
            pass

        # 设置全局字体选项
        # font_type = kwargs['font_type'] if 'font_type' in kwargs else 'Arial'  # 默认字体为sans-serif
        font_type = kwargs['font_type'] if 'font_type' in kwargs else 'sans-serif'  # 默认字体为sans-serif
        font_config = {'font.family': font_type, 'font.weight': 200}  # font.family设定所有字体为font_type
        plt.rcParams.update(font_config)  # 但是对于希腊字母(e.g. α, β, γ等)跟各种数学符号之类的不适用, Latex语法如Γ会被判断为None
        # plt.rcParams['mathtext.default'] = 'regular'  # 可以通过这个选项修改所有希腊字母以及数学符号为Times New Roman
        return

    # 这个函数可以用于画单根曲线，并确定曲线的形式，如：线型（散点还是连续曲线），线的颜色，线宽等等
    # 如有多根曲线，则可以重复调用此函数来画图
    # 这个函数的输入数据x和y必须是一维数组（也就是说(x,y)是二维数组）
    def Visualize(self,x,y,**kwargs):
        x = np.array(x)  # 将输入的数据转换为数组，以防出错
        y = np.array(y)

        # 接下来是一些曲线参数
        curve = kwargs['curve'] if 'curve' in kwargs else 'curve'  # 图谱类型参数，默认为平滑曲线图
        # 如果是图线为平滑曲线，可以通过以下列两个参数设置样式
        linestyle = kwargs['linestyle'] if 'linestyle' in kwargs else '-'  # 线型参数，默认为实线
        linewidth = kwargs['linewidth'] if 'linewidth' in kwargs else 2.0  # 控制线宽的参数
        # 如果是图线为散点图，则可以通过下列两个参数设置样式
        marker = kwargs['marker'] if 'marker' in kwargs else '.'  # 散点参数，默认为圆点
        markersize = kwargs['markersize'] if 'markersize' in kwargs else 100.0  # 散点大小参数
        color = kwargs['color'] if 'color' in kwargs else 'k'      # 颜色参数，默认为黑色
        alpha = kwargs['alpha'] if 'alpha' in kwargs else 1.0      # 曲线透明度

        # 这个参数在画多曲线图时很有用，可以控制哪根线在顶层哪根在底层
        zorder = kwargs['zorder'] if 'zorder' in kwargs else 1     # zorder越低,图层位置越来靠下；越高越靠表面

        # 通过图例标签控制是否分开单独标注图例
        if 'label' in kwargs:
            if curve == 'scatter':  # 'scatter'字符串可以控制画散点图
                plt.scatter(x, y, marker=marker, s=markersize, color=color, alpha=alpha, label=kwargs['label'],
                            zorder=zorder)
            elif curve == 'spline':  # 'spline'字符串可以控制画点线图
                plt.plot(x, y, linestyle=linestyle, linewidth=linewidth, color=color, alpha=alpha,
                         marker=marker, label=kwargs['label'], zorder=zorder)
            else:
                plt.plot(x, y, linestyle=linestyle, linewidth=linewidth, color=color, alpha=alpha,
                         label=kwargs['label'], zorder=zorder)
        else:
            if curve == 'scatter':  # 'scatter'字符串可以控制画散点图
                plt.scatter(x,y,marker=marker,s=markersize,color=color,alpha=alpha,zorder=zorder)
            elif curve == 'spline':  # 'spline'字符串可以控制画点线图
                plt.plot(x,y,linestyle=linestyle,linewidth=linewidth,color=color,alpha=alpha,marker=marker,zorder=zorder)
            else:
                plt.plot(x,y,linestyle=linestyle,linewidth=linewidth,color=color,alpha=alpha,zorder=zorder)

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
        legend_size = kwargs['legend_size'] if 'legend_size' in kwargs else 16  # 控制图例大小的参数
        if legend == 'True':
            plt.legend(loc=location,labels=labels,fontsize=legend_size,frameon=False)  # 设置图例
        else:
            pass

        # 控制x轴跟y轴坐标轴名称的模块
        label_size = kwargs['label_size'] if 'label_size' in kwargs else 16  # 控制坐标轴名称大小的参数
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
        tick_size = kwargs['tick_size'] if 'tick_size' in kwargs else 16  # 控制x轴跟y轴刻度大小的参数
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
            plt.title(kwargs['title'],size=18)
        else:
            pass

        plt.tight_layout()  # 防止画图时，图像分布失衡，部分文字显示被遮挡的情况

        return

    # 图像保存函数
    def SavingFigure(self,saving_directory,**kwargs):
        filename = kwargs['filename'] if 'filename' in kwargs else 'Untitled'  # 文件名
        format = kwargs['format'] if 'format' in kwargs else 'eps'  # 储存格式
        dpi = kwargs['dpi'] if 'dpi' in kwargs else 600  # 分辨率

        saving_address = saving_directory+filename+'.'+format  # 图像文件要储存到的绝对地址

        plt.savefig(saving_address, dpi=dpi, format=format)

        return

if __name__=='__main__':
    x1 = np.linspace(0,5,100)
    x2 = np.linspace(0,10,100)
    y1 = np.cos(x1)
    y2 = np.sin(x2)


    def cmyk_to_rgb(c, m, y, k, cmyk_scale=100, rgb_scale=255):
        r = rgb_scale * (1.0 - c / float(cmyk_scale)) * (1.0 - k / float(cmyk_scale))
        g = rgb_scale * (1.0 - m / float(cmyk_scale)) * (1.0 - k / float(cmyk_scale))
        b = rgb_scale * (1.0 - y / float(cmyk_scale)) * (1.0 - k / float(cmyk_scale))
        return np.array([r, g, b])/255.0
    print(cmyk_to_rgb(78,65,44,3,100))

    fig = plot()
    #print(np.array([x1]))

    fig.GlobalSetting()  # 引入全局画图参数

    # color = ''
    # color = fig.RGB(142.5195, 173.502, 206.55)
    color = fig.CMYK_to_RGB(0,0,0,33)
    # color = 'brown'

    # 红-'brown', 灰-'grey'

    # 应注意，唯有当x1与x2的长度一样的时候，才能把两者合成一个二维数组
    fig.Visualize(np.array([x1,x2]),np.array([y1,y2]),color=color)