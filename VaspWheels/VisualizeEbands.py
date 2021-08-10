# This code is written for visualization of electronic band structures from V.A.S.P. computation results.

import matplotlib.pyplot as plt
from VaspWheels import GetKpath
from VaspWheels import GetEbands

# 一些用于文章级结果图的matplotlib参数，由于这些参数都是通用的，所以可以作为全局变量设置
plt.rcParams['xtick.direction'] = 'in'  # 将x轴的刻度线方向设置向内
plt.rcParams['ytick.direction'] = 'in'  # 将y轴的刻度线方向设置向内
font_config = {'font.family':'Times New Roman'}  # font.family设定所有字体为Times New Roman
plt.rcParams.update(font_config)  # 但是对于希腊字母(e.g. α, β, γ等)跟各种数学符号之类的不适用, Latex语法如$\Gamma$会被判断为None
plt.rcParams['mathtext.default'] = 'regular'  # 可以通过这个选项修改所有希腊字母以及数学符号为Times New Roman

GetK = GetKpath.Kpath()
GetE = GetEbands.Ebands()

class Plotting:
    def __init__(self):
        self.name = Plotting

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
            plt.ylabel('$E-E_{f}$ $\mathrm{(eV)}$',size=24,fontdict={'style':'italic'})  # style选项选用italic启动西文斜体
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
    Kpoints = [r'$\Gamma$','M', 'K', r'$\Gamma$', 'A', 'L', 'H', 'A']
    path = [[0, 0, 0], [0.5, 0, 0], [1.0 / 3.0, 1.0 / 3.0, 0], [0, 0, 0], [0, 0, 0.5], [0.5, 0, 0.5], [1.0 / 3.0, 1.0 / 3.0, 0.5], [0, 0, 0.5]]
    lattice = ['HEX', [3.16, 3.16, 12.9, 90, 90, 120], 'primitive']
    a = plot.Ebands(EIGENVAL,path,LatticeCorrection='True',Lattice=lattice,ShiftFermi='True',Efermi=5.1,Kpoints=Kpoints,title='Band structure of bulk MoS2',latex='True')
    #print(len(a['energy'][0]))
    #print(len(a['occupation'][31]))
    # print(a[1])
    #kpath.GetKpath(saving_directory,path,59)