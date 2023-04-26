import matplotlib.pyplot as plt
import numpy as np
from VaspWheels.colors import xkcd_rgb, crayons
from VaspWheels import GetKpath,GetElectronicBands,Visualization,VisualizeBands

GK = GetKpath.vasp()              # 调用GetKpath模块（可以获取K点路径）
GE = GetElectronicBands.vasp()    # 调用GetElectronicBands模块（可以获取能带数据）
VI = Visualization.plot()         # 调用Visualization模块（可视化基础包）
VB = VisualizeBands.plot_bands()  # 调用VisualizeBands模块（能带可视化专用包）

class data_analysis:
    ''' This class of functions are designed to analyze energy band data. '''
    def __init__(self,working_place,data_location,lattice,HSP_path,shift_Fermi=True,color=crayons['Navy Blue'],y_major=2):
        self.name = data_analysis

        # 以字典形式记录的计算结果所在的主目录
        data_directory = {'MMW502': 'D:/Projects/OptoTransition/Data',  # 办公室电脑
                          'JCPGH1': 'D:/Projects/OptoTransition/Data',  # 宿舍电脑
                          'Macbook': '/Users/liusongwei/Desktop/OptoTransition/Data',  # Macbook
                          'Zhuhai': 'D:/PhD_research/OptoTransition/Data'}  # 珠海电脑

        self.EIGENVAL = data_directory[working_place] + '/' + data_location + '/EIGENVAL'  # 数据文件（EIGENVAL）的绝对地址

        # 能带图保存目录
        saving_directory_dict = {'MMW502': 'D:/Projects/OptoTransition/Data/Figures/Band structure',  # 办公室电脑
                                 'JCPGH1': 'D:/Projects/OptoTransition/Gallery',    # 宿舍电脑
                                 'Macbook': '/Users/liusongwei/Desktop/OptoTransition/Data/Figures/Band structure',  # Macbook
                                 'Zhuhai': 'D:/PhD_research/OptoTransition/Data'}   # 珠海电脑

        self.saving_directory = saving_directory_dict[working_place]  # 如要保存数据图像，要指定保存路径

        # 存放晶体结构参数的字典
        lattice_dict = {'HEX': ['HEX', [3.16, 3.16, 12.9, 90, 90, 120], 'primitive'],
                        'ORT': ['ORT', [3.16, 5.47, 12.9, 90, 90, 90], 'unitcell']}
        self.lattice = lattice_dict[lattice]

        # 存放高对称点路径的字典
        HighSymPoint = {'HEX_2D': [r'$\Gamma$', 'M', 'K', r'$\Gamma$'],
                        'HEX_3D': [r'$\Gamma$', 'M', 'K', r'$\Gamma$', 'A', 'L', 'H', 'A'],
                        'ORT': [r'$\Gamma$', 'X', 'S', 'Y', r'$\Gamma$', 'S'],
                        'ORT_1': [r'$\Gamma$', 'Y', 'S', 'X', r'$\Gamma$', 'S'],
                        'ORT_2': [r'$\Gamma$', 'X', 'S', r'$\Gamma$', 'Y']}
        self.HSP_path = HighSymPoint[HSP_path]  # HSP - short for High Symmetry Point

        # 控制是否进行费米面调零的选项
        self.shift_Fermi = shift_Fermi

        # 从VASP计算结果中提取数据
        # 分析整理能带计算结果
        bands_dict = GE.GetEbands(self.EIGENVAL)  # 调用GetElectronicBands.vasp()中的函数提取能带计算数据
        self.num_bands = bands_dict['num_bands']  # 提取能带总数
        self.num_kpoints = bands_dict['num_kpoints']  # 提取K点总数
        self.Kpath = bands_dict['Kpath']  # K点路径
        self.bands = bands_dict['bands']  # 能带具体的能量值

        # 调用GetElectronicBands.vasp()中的函数对能带计算结果进行分析（寻找价带顶跟导带底以及计算带隙等）
        Eg, Ev_max, Ec_min, extremum_location = GE.GetBandgap(self.EIGENVAL, mode='occupation')
        self.Eg, self.Ev_max, self.Ec_min, self.extremum_location = [Eg, Ev_max, Ec_min, extremum_location]  # 转换为实例函数

        # 画图参数
        self.color=color
        self.y_major=y_major

    def GetBandgap(self): return self.Eg

    def Plot_EnergyBands(self):
        # 生成投影到一维的K点路径
        num_segments = len(self.HSP_path) - 1
        Kpath_projected, Knodes_projected = GK.ProjectKpath(self.Kpath, num_segments, LatticeCorrection='True', Lattice=self.lattice)

        if self.shift_Fermi:
            bands_shifted = GE.ShiftFermiSurface(self.bands, self.Ev_max)  # 费米面调零
            VB.Electron_bands(Kpath_projected, bands_shifted, Knodes_projected, ylim=(-2, 5), y_major_tick=self.y_major, HighSymPoint=self.HSP_path, color=self.color)
        else:
            VB.Electron_bands(Kpath_projected, self.bands, Knodes_projected, ylim=(-2, 5), y_major_tick=self.y_major, HighSymPoint=self.HSP_path, color=self.color)

class data_recording:
    ''' This class of function is designed for recording data. '''  #  这一行的缩进也要跟下一行对齐
    def __init__(self):
        self.name = data_recording

    # 用于保存数据的函数
    def Save_Data(self,saving_directory,file_name,data,sep=' '):
        file_address = saving_directory + '/' + file_name + '.txt'
        np.savetxt(file_address,data,delimiter=sep)

    # 用于保存图像的函数
    def Save_Figure(self, saving_directory, file_name, dpi=600, format=('eps', 'jpg')):
        for i in format:
            file_address = saving_directory + '/' + file_name + '.' + str(i)
            plt.savefig(file_address, dpi=dpi, format=i)

if __name__=='__main__':
    saving_filename = 'MoS2_bilayer_0.500'  # 数据文件保存时的名称

    data_directory = 'Stark_effect/2-layer/GSE_Bilayer_SOC'
    # data_directory = 'GSE/2_layer/GSE_Bilayer_SYM'

    #E_field = ['E_0.025', 'E_0.050', 'E_0.075', 'E_0.100', 'E_0.125', 'E_0.150', 'E_0.175', 'E_0.200', 'E_0.225', 'E_0.250',
               #'E_0.275', 'E_0.300', 'E_0.325', 'E_0.350', 'E_0.375', 'E_0.400', 'E_0.425', 'E_0.450', 'E_0.475', 'E_0.500',
               #'E_0.525', 'E_0.550']
    #E_field = ['0.000', '0.025', '0.050', '0.075', '0.100', '0.125', '0.150', '0.175', '0.200', '0.225','0.250',
               #'0.275', '0.300', '0.325', '0.350', '0.375', '0.400', '0.425', '0.450', '0.475','0.500','0.525', '0.550']
    E_field = ['0.200']

    color = ['#1f77b4', '#d62728', '#2ca02c', '#9467bd']

    Bandgap = []
    for i in E_field:
        data_location = data_directory+'/E_'+i
        DA = data_analysis('MMW502',data_location,'HEX','HEX_2D',shift_Fermi=True,color=color[2])
        Bandgap.append([float(i)*10.0,DA.GetBandgap()])

        DA.Plot_EnergyBands()

    # DA.Save_Figure(saving_filename)

    # print(Bandgap)
    DR = data_recording()
    saving_directory = 'D:/OneDrive/OneDrive - The Chinese University of Hong Kong/Desktop/Test'
    # DR.Save_Data(saving_directory,'GSE_2_SOC_SYM',Bandgap)
    DR.Save_Figure(saving_directory,'GSE_2_SOC_0.200')