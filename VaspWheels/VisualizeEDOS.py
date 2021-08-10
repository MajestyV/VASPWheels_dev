# This code is written for visualization of electronic band structures from V.A.S.P. computation results.

import matplotlib.pyplot as plt
from VaspWheels import GetEDOS

# 一些用于文章级结果图的matplotlib参数，由于这些参数都是通用的，所以可以作为全局变量设置
plt.rcParams['xtick.direction'] = 'in'  # 将x轴的刻度线方向设置向内
plt.rcParams['ytick.direction'] = 'in'  # 将y轴的刻度线方向设置向内
font_config = {'font.family':'Times New Roman'}  # font.family设定所有字体为Times New Roman
plt.rcParams.update(font_config)  # 但是对于希腊字母(e.g. α, β, γ等)跟各种数学符号之类的不适用, Latex语法如$\Gamma$会被判断为None
plt.rcParams['mathtext.default'] = 'regular'  # 可以通过这个选项修改所有希腊字母以及数学符号为Times New Roman

GetEDOS = GetEDOS.EDOS()

class Plotting:
    def __init__(self):
        self.name = Plotting

    # This function is written to shift the Fermi energy to 0. And the whole x-axis of DOS will be shift as well.
    def ShiftFermi(self,energy,Fermi_energy):
        shifted_energy = []
        for i in range(len(energy)):
            shifted_energy.append(energy[i]-Fermi_energy)
        return shifted_energy

    def EDOS(self,DOSCAR,**kwargs):
        # 提取态密度计算结果以及各种参数
        dos_result = GetEDOS.GetData(DOSCAR)
        Ef = dos_result['Efermi']  # 提取费米能级
        energy = dos_result['energy']  # 提取能量值作为横坐标
        dos = dos_result['DOS']  # 提取总态密度的计算结果
        tos = dos_result['integrated DOS']  # 提取总态数目(Total number of states, TOS - DOS的积分)的计算结果

        # 投影态密度的读取选项
        

        # 费米能调零选项
        shift = kwargs['ShiftFermi'] if 'ShiftFermi' in kwargs else 'False'
        if shift == 'True':
            energy = self.ShiftFermi(energy,Ef)
        else:
            pass

        # 画图参数
        xlim = kwargs['xlim'] if 'xlim' in kwargs else [energy[0],energy[len(energy)-1]]  # Python计数从0开始，所以要减1
        xmin, xmax = xlim
        ylim = kwargs['ylim'] if 'ylim' in kwargs else [0,max(dos)]  # Y轴范围
        ymin, ymax = ylim
        color = kwargs['color'] if 'color' in kwargs else 'b'

        # 启用Latex编译与否，启用了Latex语法之后，编译会极度慢，所以通常只有画文章级的图时才启用
        latex = kwargs['latex'] if 'latex' in kwargs else 'False'
        font_latex = {'text.usetex':latex}  # text.usetex为True启用latex语法，为False则不启用
        plt.rcParams.update(font_latex)

        plt.plot(energy,dos,linewidth=1,color=color)
        plot_tos = kwargs['plot_TOS'] if 'plot_TOS' in kwargs else 'False'
        if plot_tos == 'True':
            plt.plot(energy,tos,linewidth=1,color='k')
        else:
            pass
        if shift == 'True':
            plt.vlines(0,ymin,ymax,linewidth=0.5,linestyles='dashed',colors='k')  # The Fermi energy have been shifted to 0.
            plt.xlabel('$E-E_{f}$ $\mathrm{(eV)}$',size=24,fontdict={'style':'italic'})  # style选项选用italic启动西文斜体
        else:
            plt.vlines(Ef,ymin,ymax,linewidth=0.5,linestyles='dashed',colors='k')
            plt.xlabel('Energy (eV)',size=24)
        plt.ylabel('DOS (states/eV)', size=24)
        plt.xticks(size=14)
        plt.yticks([])
        plt.xlim(xmin,xmax)
        plt.ylim(ymin,ymax)
        if 'title' in kwargs:
            plt.title(kwargs['title'],size=26)
        else:
            pass

        plt.tight_layout()  # 用于调整图像位置，以免坐标轴的标签被遮挡

        return

if __name__=='__main__':
    DOSCAR = 'D:/OneDrive/OneDrive - The Chinese University of Hong Kong/Desktop/Testing/DOSCAR'
    plot = Plotting()
    a = plot.EDOS(DOSCAR,ShiftFermi='True',plot_TOS='False',xlim=(-5,5),ylim=(0,20),title='DOS of bulk MoS2')
    #print(len(a['energy'][0]))
    #print(len(a['occupation'][31]))
    # print(a[1])
    #kpath.GetKpath(saving_directory,path,59)