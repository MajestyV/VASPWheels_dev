# This code is written to visualize band structures, both electronic or vibrational.
# Specialized for handling calculation results gained from V.A.S.P. and Phonopy.

import numpy as np
import matplotlib.pyplot as plt
from VaspWheels import GetKpath
from VaspWheels import GetEbands
from Visualize import Visualization

####################################################################################################################
GK = GetKpath.Kpath()      # 调用GetKpath模块
GE = GetEbands.Ebands()    # 调用GetEbands模块
VI = Visualization.plot()  # 调用Visualization模块
#####################################################################################################################

class plotting:
    def __init__(self):
        self.name = plotting

    # 这个函数可以用于可视化电子能带
    def Ebands(self,EIGENVAL,Kpath,**kwargs):
        # 提取能带计算结果以及各种参数
        bands = GE.GetData(EIGENVAL)
        nbands = bands['number']  # 提取能带总数
        nkpoints_total = bands['num kpoints']  # 提取K点总数
        nnodes = len(Kpath)  # 高对称点数
        npoints = int((nkpoints_total-nnodes)/(nnodes-1))  # 两个高对称点中间的取点数 = (K点总数-高对称点数)/(高对称点数-1)
        energy = bands['energy']  # 能带具体的能量值

        # 费米能调零选项设置
        shift = kwargs['ShiftFermi'] if 'ShiftFermi' in kwargs else 'False'
        Ef = kwargs['Efermi'] if 'Efermi' in kwargs else 0
        if shift == 'True':
            energy = self.ShiftFermi(energy,Ef)
        else:
            pass

        # 利用GetKpath模块确定K点路径（X轴）
        correction = kwargs['LatticeCorrection'] if 'LatticeCorrection' in kwargs else 'False'  # 晶格修正选项
        lattice = kwargs['Lattice'] if 'Lattice' in kwargs else ['Cubic', [1, 1, 1, 90, 90, 90], 'primitive']
        k,knodes = GK.ProjectKpath(Kpath,npoints,LatticeCorrection=correction,Lattice=lattice)  # 生成投影到一维的K点路径

        # 画图参数
        HSP = kwargs['Kpoints'] if 'Kpoints' in kwargs else ['P'+str(n+1) for n in range(len(knodes))]  # HSP - high symmetry point
        xlim = (k[0],k[len(k)-1])  # X轴范围
        ylim = kwargs['ylim'] if 'ylim' in kwargs else (-20,20)  # Y轴范围
        color = kwargs['color'] if 'color' in kwargs else np.array([70,148,203])/255.0  # 控制颜色

        VI.GlobalSetting(bottom_tick=False,y_major_tick=2)  # 利用Visualization模块引入画图全局变量

        # 画Visualization模块能带图
        for i in range(nbands):
            VI.Visualize(k,energy[i],color=color)

            # 画高对称点分割线
            seperate_line_color = np.array([155,165,160])/255.0
            for i in range(len(knodes)-2):  # 第一跟最后的一个高对称点跟能带图的左右边界重合，所以不必作分割线
                plt.vlines(knodes[i+1], ylim[0], ylim[1], linewidth=2, linestyles='dashed', colors=seperate_line_color)
            # 画费米面分割线
            if shift == 'True':
                plt.hlines(0, xlim[0], xlim[1], linewidth=2, linestyles='dashed',
                           colors=seperate_line_color)  # The Fermi energy have been shifted to 0.
                # plt.ylabel('$E-E_{f}$ $\mathrm{(eV)}$',size=24,fontdict={'style':'italic'})  # style选项选用italic启动西文斜体
                plt.ylabel('$E-E_{f}$ (eV)', size=20)  # style选项选用italic启动西文斜体
            else:
                plt.hlines(Ef, xlim[0], xlim[1], linewidth=2, linestyles='dashed', colors=seperate_line_color)
                plt.ylabel('$E-E_{f}$ (eV)', size=20)

            # 对于能带图，有些参数Visualization模块无法设置，因此在此利用matplotlib进行修改
            plt.xticks(knodes, HSP, size=20)
            if 'title' in kwargs:
                plt.title(kwargs['title'], size=24)
            else:
                pass

        # 利用Visualization对图像细节进行修改
        VI.FigureSetting(xlim=xlim,ylim=ylim)

        return

    def VisualizePhononBand(self,band_yaml,degree_of_freedom=3,**kwargs):
        raw_data = self.ReadPhonopyData(band_yaml)
        q_projected, frequency, nbands, nqpoint, npath = self.RearrangePhonopyData(raw_data,degree_of_freedom)

        # HSP - High Symmetry Point
        HSP_notation = kwargs['Kpoints'] if 'Kpoints' in kwargs else ['P' + str(n + 1) for n in range(npath+1)]
        HSP_position = [q_projected[0]]+[q_projected[int(nqpoint/npath)*i-1] for i in range(1,npath)]+[q_projected[len(q_projected)-1]]
        # 把初始点跟终点都包括进去

        xmin = q_projected[0]  # X轴范围
        xmax = q_projected[len(q_projected) - 1]
        ylim = kwargs['ylim'] if 'ylim' in kwargs else [0, 15]  # Y轴范围
        ymin, ymax = ylim
        color = kwargs['color'] if 'color' in kwargs else 'k'
        label = kwargs['label'] if 'label' in kwargs else None
        linewidth = kwargs['linewidth'] if 'linewidth' in kwargs else '0.6'

        label_band = kwargs['label_band'] if 'label_band' in kwargs else 'False'
        bands_labelled = kwargs['bands_labelled'] if 'bands_labelled' in kwargs else None
        labelling_color = kwargs['labelling_color'] if 'labelling_color' in kwargs else 'r'

        # 单位转换(太赫兹到波数)：1 THz= 33.35641 cm-1
        unit = kwargs['unit'] if 'unit' in kwargs else 'THz'
        if unit == 'cm-1':
            frequency = [[frequency[i][j]*33.35641 for j in range(len(frequency[i]))] for i in range(len(frequency))]
        else:
            pass

        for n in range(nbands):
            if label_band == 'True':
                if n+1 in bands_labelled:
                    #if bands_labelled.index(n+1) == 0:
                        #plt.plot(q_projected, frequency[n], linewidth=linewidth, color=labelling_color, label='Raman active')
                    #else:
                        #plt.plot(q_projected, frequency[n], linewidth=linewidth, color=labelling_color)
                    plt.plot(q_projected, frequency[n], linewidth=linewidth, color=labelling_color)
                else:
                    plt.plot(q_projected, frequency[n], linewidth=linewidth, color=color)
            else:
                if label and n==0:
                    plt.plot(q_projected,frequency[n],linewidth=linewidth,color=color,label=label)
                else:
                    plt.plot(q_projected,frequency[n],linewidth=linewidth,color=color)
        plt.xlim(xmin,xmax)
        plt.ylim(ymin,ymax)

        plt.vlines(HSP_position,ymin,ymax,linewidth=0.5,linestyles='dashed',colors='k')
        plt.hlines(0,xmin,xmax,linewidth=0.5,linestyles='dashed',colors='k')

        plt.xticks(HSP_position, HSP_notation, size=20)
        plt.yticks(size=14)

        if unit == 'cm-1':
            plt.ylabel('$\omega$ ($cm^{-1}$)', size=18)
        else:
            plt.ylabel('Frequency (THz)', size=18)

        if 'title' in kwargs:
            plt.title(kwargs['title'],size=26)
        else:
            pass

        return HSP_position, HSP_notation

if __name__=='__main__':
    EIGENVAL = 'D:/MaterialsGallery/Testing/MoS2_monolayer_test/result_double_cell/EIGENVAL'
    plot = Plotting()
    #Kpoints = [r'$\Gamma$','M', 'K', r'$\Gamma$', 'A', 'L', 'H', 'A']
    #path = [[0, 0, 0], [0.5, 0, 0], [1.0 / 3.0, 1.0 / 3.0, 0], [0, 0, 0], [0,0,1/2.0], [1/2.0,0,1/2.0], [1/3.0, 1/3.0, 1/2.0], [0,0,1/2.0]]
    Kpoints = [r'$\Gamma$', 'M', 'K', r'$\Gamma$']
    path = [[0, 0, 0], [0.5, 0, 0], [1.0 / 3.0, 1.0 / 3.0, 0], [0, 0, 0]]
    lattice = ['HEX', [3.16, 3.16, 12.9, 90, 90, 120], 'primitive']
    a = plot.Ebands(EIGENVAL,path,LatticeCorrection='True',Lattice=lattice,ShiftFermi='False',Efermi=6.685,Kpoints=Kpoints,ylim=(-5,5),title='Band structure of 7-layer MoS2',latex='False')
    #print(len(a['energy'][0]))
    #print(len(a['occupation'][31]))
    # print(a[1])
    #kpath.GetKpath(saving_directory,path,59)