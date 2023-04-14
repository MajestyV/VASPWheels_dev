import matplotlib.pyplot as plt
from VaspWheels import GetKpath,GetElectronicBands,Visualization,VisualizeBands

GK = GetKpath.vasp()              # 调用GetKpath模块（可以获取K点路径）
GE = GetElectronicBands.vasp()    # 调用GetElectronicBands模块（可以获取能带数据）
VI = Visualization.plot()         # 调用Visualization模块（可视化基础包）
VB = VisualizeBands.plot_bands()  # 调用VisualizeBands模块（能带可视化专用包）

class data_analysis:
    ''' This class of functions are designed to analyze energy band data. '''
    def __init__(self,working_place,data_location,lattice,HSP_path,shift_Fermi=True):
        self.name = data_analysis

        # 以字典形式记录的计算结果所在的主目录
        data_directory = {'MMW502': 'D:/Projects/OptoTransition/Data',  # 办公室电脑
                          'JCPGH1': 'D:/Projects/OptoTransition/Data',  # 宿舍电脑
                          'Macbook': '/Users/liusongwei/Desktop/OptoTransition/Data'}  # Macbook

        self.EIGENVAL = data_directory[working_place] + '/' + data_location + '/EIGENVAL'  # 数据文件（EIGENVAL）的绝对地址

        # 能带图保存目录
        saving_directory_dict = {'MMW502': 'D:/Projects/OptoTransition/Data/Figures/Band structure',  # 办公室电脑
                                 'JCPGH1': 'D:/Projects/OptoTransition/Gallery',    # 宿舍电脑
                                 'Macbook': '/Users/liusongwei/Desktop/OptoTransition/Data/Figures/Band structure'}    # Macbook

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

    def Plot_EnergyBands(self):
        # 分析整理能带计算结果
        bands_dict = GE.GetEbands(self.EIGENVAL)  # 提取能带计算结果以及各种参数
        num_bands = bands_dict['num_bands']  # 提取能带总数
        num_kpoints = bands_dict['num_kpoints']  # 提取K点总数
        Kpath = bands_dict['Kpath']  # K点路径
        bands = bands_dict['bands']  # 能带具体的能量值

        # 生成投影到一维的K点路径
        num_segments = len(self.HSP_path)-1
        Kpath_projected, Knodes_projected = GK.ProjectKpath(Kpath, num_segments, LatticeCorrection='True', Lattice=self.lattice)

        Eg, Ev_max, Ec_min, extremum_location = GE.GetBandgap(self.EIGENVAL, mode='occupation')  # 寻找价带顶跟导带底以及计算带隙

        if self.shift_Fermi:
            bands_shifted = GE.ShiftFermiSurface(bands, Ev_max)  # 费米面调零
            VB.Electron_bands(Kpath_projected, bands_shifted, Knodes_projected, ylim=(-2, 5), y_major_tick=1,HighSymPoint=self.HSP_path)
        else:
            VB.Electron_bands(Kpath_projected, bands, Knodes_projected, ylim=(-2, 5), y_major_tick=1,HighSymPoint=self.HSP_path)

    # 用于保存图像的函数
    def Save_Figure(self,filename,dpi=600,format=('eps','jpg')):
        if isinstance(format,str):
            address = self.saving_directory + '/' + filename + '.' + str(format)
            plt.savefig(address, dpi=dpi, format=format)
        else:
            for i in format:
                address = self.saving_directory + '/' + filename + '.' + str(i)
                plt.savefig(address, dpi=dpi, format=i)

if __name__=='__main__':
    saving_filename = 'MoS2_bilayer_0.500'  # 数据文件保存时的名称

    data_location = 'Stark_effect/DipoleSheet/GSE_Bilayer/E_0.500'

    DA = data_analysis('JCPGH1',data_location,'HEX','HEX_2D',shift_Fermi=True)

    DA.Plot_EnergyBands()

    DA.Save_Figure(saving_filename)