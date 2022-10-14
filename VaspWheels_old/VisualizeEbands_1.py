# This code is written for visualization of electronic band structures from V.A.S.P. computation results.

import matplotlib.pyplot as plt
from VaspWheels import GetKpath
from VaspWheels import GetEbands
from Visualize import Visualization

GetK = GetKpath.Kpath()
GetE = GetEbands.Ebands()
plot = Visualization.plot()

class ebands:
    def __init__(self):
        self.name = ebands

    # This function is written to shift the Fermi energy to 0. And the whole band structure will be shift as well.
    # Example input: energy = [[band 1], [band 2], [band 3]......], Fermi_energy = Ef
    def ShiftFermi(self,energy,Fermi_energy):
        nbands = len(energy)  # number of bands
        nkpoints = len(energy[0])  # number of k points calculated
        shifted_energy = [[] for n in range(nbands)]
        for i in range(nbands):
            for j in range(nkpoints):
                shifted_energy[i].append(energy[i][j]-Fermi_energy)
        return shifted_energy

    def Ebands(self,EIGENVAL,Kpath,**kwargs):
        # 提取能带计算结果以及各种参数
        bands = GetE.GetData(EIGENVAL)
        nbands = bands['number']  # 提取能带总数
        nkpoints_total = bands['num kpoints']  # 提取K点总数
        nnodes = len(Kpath)  # 高对称点数
        npoints = int((nkpoints_total-nnodes)/(nnodes-1))  # 两个高对称点中间的取点数 = (K点总数-高对称点数)/(高对称点数-1)
        energy = bands['energy']  # 能带具体的能量值

        # 费米能调零选项
        shift = kwargs['ShiftFermi'] if 'ShiftFermi' in kwargs else 'False'
        Ef = kwargs['Efermi'] if 'Efermi' in kwargs else 0
        if shift == 'True':
            energy = self.ShiftFermi(energy,Ef)
        else:
            pass

        # 确定K点路径（X轴）
        correction = kwargs['LatticeCorrection'] if 'LatticeCorrection' in kwargs else 'False'  # 晶格修正选项
        lattice = kwargs['Lattice'] if 'Lattice' in kwargs else ['Cubic', [1, 1, 1, 90, 90, 90], 'primitive']
        k,knodes = GetK.ProjectKpath(Kpath,npoints,LatticeCorrection=correction,Lattice=lattice)  # 生成投影到一维的K点路径

        # 画图参数
        HSP = kwargs['Kpoints'] if 'Kpoints' in kwargs else ['P'+str(n+1) for n in range(len(knodes))]  # HSP - high symmetry point
        xmin = k[0]  # X轴范围
        xmax = k[len(k)-1]
        ylim = kwargs['ylim'] if 'ylim' in kwargs else [-20,20]  # Y轴范围
        ymin, ymax = ylim
        linewidth = kwargs['linewidth'] if 'linewidth' in kwargs else 0.5  # 控制线宽
        color = kwargs['color'] if 'color' in kwargs else 'b'  # 控制颜色

        plot.GlobalSetting()  # 引入plot类别函数中，画图所需的全局变量

        for i in range(nbands):
            plot.Visulize(k,energy[i],linewidth=linewidth,color=color)
        for i in range(len(knodes)-1):  # 最后的一个高对称点跟图的右边界重合，所以不必作分割线
            plt.vlines(knodes[i],ymin,ymax,linewidth=0.5,linestyles='dashed',colors='k')
        if shift == 'True':
            plt.hlines(0,xmin,xmax,linewidth=0.5,linestyles='dashed',colors='k')  # The Fermi energy have been shifted to 0.
            # plt.ylabel('$E-E_{f}$ $\mathrm{(eV)}$',size=24,fontdict={'style':'italic'})  # style选项选用italic启动西文斜体
            plt.ylabel('$E-E_{f}$ (eV)', size=24)  # style选项选用italic启动西文斜体
        else:
            plt.hlines(Ef,xmin,xmax,linewidth=0.5,linestyles='dashed',colors='k')
            plt.ylabel('$E-E_{f}$ (eV)',size=24)

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