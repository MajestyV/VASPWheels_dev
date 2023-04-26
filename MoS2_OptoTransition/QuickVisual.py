########################################################################################################################
# 模块调用
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator
from VaspWheels.colors import xkcd_rgb, crayons
# from VaspWheels import GetKpath,GetElectronicBands,Visualization,VisualizeBands

# GK = GetKpath.vasp()              # 调用GetKpath模块（可以获取K点路径）
# GE = GetElectronicBands.vasp()    # 调用GetElectronicBands模块（可以获取能带数据）
# VI = Visualization.plot()         # 调用Visualization模块（可视化基础包）
# VB = VisualizeBands.plot_bands()  # 调用VisualizeBands模块（能带可视化专用包）

class QuickVisual:
    ''' This class of function is designed for visualizing data in a uniform format via matplotlib. '''
    def __init__(self,x_major=10.0,y_major=10.0,hide_tick='False',hide_ticklabel='False'):
        self.name = QuickVisual

        # Global settings
        # 设置刻度线方向
        plt.rcParams['xtick.direction'] = 'in'  # 将x轴的刻度线方向设置向内
        plt.rcParams['ytick.direction'] = 'in'  # 将y轴的刻度线方向设置向内
        # 确定要显示刻度线的轴并设置主次刻度线长度
        plt.tick_params(bottom=True, top=False, left=True, right=False)
        plt.tick_params(which='major', length=5)  # 设置主刻度长度
        plt.tick_params(which='minor', length=2)  # 设置次刻度长度

        # 创建图例对象
        ax = plt.subplot(111)  # 注意有些参数（比如刻度）一般都在ax中设置,不在plot中设置
        if hide_tick == 'x':
            ax.set_xticks([])  # 设置x轴刻度为空
        elif hide_tick == 'y':
            ax.set_yticks([])  # 设置y轴刻度为空
        elif hide_tick == 'both':
            ax.set_xticks([])  # 设置x轴刻度为空
            ax.set_yticks([])  # 设置y轴刻度为空
        else:
            # 设置主刻度
            x_major_locator = MultipleLocator(x_major)  # 将x主刻度标签设置为x_major_tick的倍数
            y_major_locator = MultipleLocator(y_major)  # 将y主刻度标签设置为y_major_tick的倍数
            ax.xaxis.set_major_locator(x_major_locator)
            ax.yaxis.set_major_locator(y_major_locator)
            # 设置次刻度
            x_minor_locator = MultipleLocator(x_major/5.0)  # 将x主刻度标签设置为x_major_tick/5.0的倍数
            y_minor_locator = MultipleLocator(y_major/5.0)  # 将y主刻度标签设置为y_major_tick/5.0的倍数
            ax.xaxis.set_minor_locator(x_minor_locator)
            ax.yaxis.set_minor_locator(y_minor_locator)

        # 设置刻度文本选项
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
        font_config = {'font.family': 'Arial', 'font.weight': 200}  # font.family设定所有字体为font_type
        plt.rcParams.update(font_config)  # 但是对于希腊字母(e.g. α, β, γ等)跟各种数学符号之类的不适用, Latex语法如Γ会被判断为None

    # def plot(self,x,y,xlim,ylim):

class data_recording:
    ''' This class of function is designed for recording data. '''
    def __init__(self):
        self.name = data_recording

    # 用于保存图像的函数
    def Save_Figure(self,saving_directory,file_name,dpi=600,format=('eps','jpg')):
        for i in format:
            file_address = saving_directory + '/' + file_name + '.' + str(i)
            plt.savefig(file_address, dpi=dpi, format=i)

if __name__=='__main__':
    # data_directory = 'D:/Projects/OptoTransition/Data/ElectricField/TOTEN'  # JCPGH1
    data_directory = 'D:/Projects/OptoTransition/Data/Total/TOTEN'  # MMW502

    file_list = ['GSE_Bilayer_TOTEN.dat','GSE_Bilayer_SYM_TOTEN.dat',
                 'GSE_Bilayer_SOC_TOTEN.dat','GSE_Bilayer_SOC_SYM_TOTEN.dat']

    data_total = []
    for file in file_list:
        file_address = data_directory+'/'+file
        data_DataFrame = pd.read_csv(file_address,header=None,sep=' ')
        data_total.append(data_DataFrame.values)

    # print(data_total[0])

    # 画图模块
    QV = QuickVisual(x_major=1.5, y_major=1.0)

    # color = ["#6495ED", "#F08080"]
    # color = ['#1f77b4', '#d62728', '#2ca02c',  '#9467bd']
    color = ['#4878d0', '#d65f5f', '#ee854a', '#6acc64', '#956cb4', '#8c613c', '#dc7ec0', '#797979', '#d5bb67', '#82c6e2']
    symbol = ['s','o','^','p']
    label = ['no SOC + no sym.', 'no SOC + sym.', 'SOC + no sym.', 'SOC + sym.']

    for i in [2,3]:
        indexing = i
        x = data_total[i][:,0]*10
        y = data_total[i][:,1]
        plt.plot(x,y,c=color[indexing],marker=symbol[indexing],label=label[indexing])

    plt.xlim(0,5.5)
    plt.ylim(-46.5,-43.5)

    plt.xlabel('Electric field (V/nm)')
    plt.ylabel('Total Energy (eV)')
    plt.legend(frameon=False)

    # 数据保存
    # print(Bandgap)
    DR = data_recording()
    saving_directory = 'D:/OneDrive/OneDrive - The Chinese University of Hong Kong/Desktop/Test'
    DR.Save_Figure(saving_directory, 'TOTEN_SOC')




#plt.vlines(0.9941748903765186*(2.0/3.0),-2.2,4.5, linewidth=2, linestyles='dashed',colors=VI.MorandiColor('Black'))
#plt.text(0.5,0.1,'K',size=16)

# 数据保存
#saving_dir_dict = {'Office': 'D:/Projects/OptoTransition/Data/Figures/Band structure',  # 办公室电脑
                   # 'C221': 'D:/Projects/OptoTransition/Data/Figures/Band structure'}    # 宿舍电脑
#VI.SavingFigure(saving_dir_dict[working_station]+'/',filename=saving_filename,format='eps')
#VI.SavingFigure(saving_dir_dict[working_station]+'/',filename=saving_filename,format='pdf')
#VI.SavingFigure(saving_dir_dict[working_station]+'/',filename=saving_filename,format='png')