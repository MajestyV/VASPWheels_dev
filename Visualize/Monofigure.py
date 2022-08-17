""" This code is designed for plotting general figures."""
# Written by Songwei Liu, on 2021-08-10.

import matplotlib.pyplot as plt
import re

# 一些用于文章级结果图的matplotlib参数，由于这些参数都是通用的，所以可以作为全局变量设置
plt.rcParams['xtick.direction'] = 'in'  # 将x轴的刻度线方向设置向内
plt.rcParams['ytick.direction'] = 'in'  # 将y轴的刻度线方向设置向内
font_config = {'font.family':'Times New Roman'}  # font.family设定所有字体为Times New Roman
plt.rcParams.update(font_config)  # 但是对于希腊字母(e.g. α, β, γ等)跟各种数学符号之类的不适用, Latex语法如Γ会被判断为None
plt.rcParams['mathtext.default'] = 'regular'  # 可以通过这个选项修改所有希腊字母以及数学符号为Times New Roman

class Plotting:
    # 输入的数据需要为字典或者列表形式
    # 列表格式为[[x],[y0],[y1],[y2]......]
    # 字典格式为{'x':[x], 'y0':[y0], 'y1':[y1], ...'yr0':[yr0], 'yr1':[yr1], 'yr2':[yr2]......}, x-y为左纵轴系，x-yr为右纵轴系(r for right)
    def __init__(self,data):
        self.name = Plotting
        if isinstance(data,list):
            self.data_dict = {'x':data[0]}
            for n in range(len(data)-1):
                self.data_dict = {'y'+str(n):data[n+1]}
        elif isinstance(data,dict):
            self.data_dict = data
        else:
            print('Please transform the input data to list or dict.')
            self.data_dict = None

    def Color(self):


    def Visualize(self,**kwargs):
        # 分配数据
        data = dict.keys(self.data_dict)

        x = self.data_dict['x']
        y = []
        yr = []
        for n in data:
            if re.match(n,'y'+'\d+'):
                y.append(self.data_dict[n])
            elif re.match(n,'yr'+r'\d+'):
                yr.append(self.data_dict[n])

        xmin = kwargs['xlim'] if 'xlim' in kwargs else self.data_dict['x']
        xmax = k[len(k)-1]
        ylim = kwargs['ylim'] if 'ylim' in kwargs else [-20,20]  # Y轴范围
        ymin, ymax = ylim
        color = kwargs['color'] if 'color' in kwargs else 'b'

        # 启用Latex编译与否，启用了Latex语法之后，编译会极度慢，所以通常只有画文章级的图时才启用
        latex = kwargs['latex'] if 'latex' in kwargs else 'False'
        font_latex = {'text.usetex':latex}  # text.usetex为True启用latex语法，为False则不启用
        plt.rcParams.update(font_latex)

        for i in range(nbands):
            plt.plot(k,energy[i],linewidth=0.5,color=color)
        for i in range(len(knodes)-1):  # 最后的一个高对称点跟图的右边界重合，所以不必作分割线
            plt.vlines(knodes[i],ymin,ymax,linewidth=0.5,linestyles='dashed',colors='k')
        if shift == 'True':
            plt.hlines(0,xmin,xmax,linewidth=0.5,linestyles='dashed',colors='k')  # The Fermi energy have been shifted to 0.
            plt.ylabel('E−Ef (eV)',size=24,fontdict={'style':'italic'})  # style选项选用italic启动西文斜体
        else:
            plt.hlines(Ef,xmin,xmax,linewidth=0.5,linestyles='dashed',colors='k')
            plt.ylabel('Energy (eV)',size=24)
        plt.xticks(knodes,HSP,size=20)
        plt.yticks(size=14)
        plt.xlim(xmin,xmax)
        plt.ylim(ymin,ymax)
        if 'title' in kwargs:
            plt.title(kwargs['title'],size=26)
        else:
            pass

        plt.tight_layout()  # 用于调整图像位置，以免坐标轴的标签被遮挡

        return

if __name__=='__main__':
    EIGENVAL = 'D:/OneDrive/OneDrive - The Chinese University of Hong Kong/Desktop/Testing/EIGENVAL'
    plot = Plotting()
    Kpoints = [r'Γ','M', 'K', r'Γ', 'A', 'L', 'H', 'A']
    path = [[0, 0, 0], [0.5, 0, 0], [1.0 / 3.0, 1.0 / 3.0, 0], [0, 0, 0], [0, 0, 0.5], [0.5, 0, 0.5], [1.0 / 3.0, 1.0 / 3.0, 0.5], [0, 0, 0.5]]
    lattice = ['HEX', [3.16, 3.16, 12.9, 90, 90, 120], 'primitive']
    a = plot.Ebands(EIGENVAL,path,LatticeCorrection='True',Lattice=lattice,ShiftFermi='True',Efermi=5.1,Kpoints=Kpoints,title='Band structure of bulk MoS2',latex='True')
    #print(len(a['energy'][0]))
    #print(len(a['occupation'][31]))
    # print(a[1])
    #kpath.GetKpath(saving_directory,path,59)