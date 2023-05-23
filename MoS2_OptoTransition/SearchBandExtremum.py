import numpy as np

import VaspWheels as vw
import matplotlib.pyplot as plt
from VaspWheels import GetKpath,GetElectronicBands

GE = GetElectronicBands.vasp()    # 调用GetElectronicBands模块（可以获取能带数据）
GK = GetKpath.vasp()              # 调用GetKpath模块（可以获取K点路径）

class full_analysis:
    ''' This class of function is designed for full analysis of electronic structure of target systems.  '''
    def __init__(self,EIGENVAL,lattice,HSP_type,dimension='3D'):
        self.name = full_analysis

        # 存放晶体结构参数的字典
        lattice_dict = {'HEX': ['HEX', [3.16, 3.16, 12.9, 90, 90, 120], 'primitive'],
                        'ORT': ['ORT', [3.16, 5.47, 12.9, 90, 90, 90], 'unitcell']}
        lattice_param = lattice_dict[lattice]

        # 从VaspWheels读取高对称点数据并存为字典，方便调用
        HighSymPoint = {'2D': vw.HSP.HighSymPoint_2D, '3D': vw.HSP.HighSymPoint_3D}
        self.HSP_path = HighSymPoint[dimension][HSP_type]  # HSP - short for High Symmetry Point

        # 数据提取模块
        # 从EIGENVAL中分析整理能带计算结果
        bands_dict = GE.GetEbands(EIGENVAL)  # 调用GetElectronicBands.vasp()中的函数提取能带计算数据
        self.num_bands = bands_dict['num_bands']  # 提取能带总数
        self.num_kpoints = bands_dict['num_kpoints']  # 提取K点总数
        self.Kpath = bands_dict['Kpath']  # K点路径
        self.bands = bands_dict['bands']  # 能带具体的能量值

        # 调用GetElectronicBands.vasp()中的函数对能带计算结果进行分析（寻找价带顶跟导带底以及计算带隙等）
        Eg, Ev_max, Ec_min, extremum_location = GE.GetBandgap(EIGENVAL, mode='occupation')
        self.Eg, self.Ev_max, self.Ec_min, self.extremum_location = [Eg, Ev_max, Ec_min, extremum_location]  # 转换为实例函数

        # 生成投影到一维的K点路径
        num_segments = len(self.HSP_path) - 1
        self.Kpath_projected, self.Knodes_projected = GK.ProjectKpath(self.Kpath, num_segments, LatticeCorrection='True',Lattice=lattice_param)
        # self.Kpath_projected = self.Kpath

    def GetData(self): return self.bands,self.Kpath

    def SearchBandExtremum(self,band_index,extremum='min'):
        band = self.bands[band_index-1].tolist()
        #for i in range(220):  # 手动去除最低能谷
            #band[i] = 100
        min_index, max_index = [band.index(min(band)),band.index(max(band))]
        if extremum == 'min':
            K_point = self.Kpath[min_index]
        elif extremum == 'max':
            K_point = self.Kpath[max_index]
        else:
            print('Error!')

        return K_point, band

if __name__=='__main__':
    # main_dir = 'D:/Projects/OptoTransition/Data/MoS2_ElectronicStructure/Trilayer/E_prop_SYM'  # MMW502
    # main_dir = 'D:/Projects/OptoTransition/Data/MoS2_ElectronicStructure/Bilayer/E_prop_SYM'  # JCPGH1
    # main_dir = 'D:/PhD_research/OptoTransition/Data/MoS2/Electronic_structure'  # Zhuhai

    data_directory = 'D:/Projects/OptoTransition/Data/Stark_effect/5-layer/GSE_Pentalayer/E_0.06'  # MMW502
    # data_directory = 'D:/Projects/OptoTransition/Data/MoS2_ElectronicStructure/Pentalayer/E_prop_SYM/'  # Test

    EIGENVAL = data_directory + '/EIGENVAL'

    FA = full_analysis(EIGENVAL, 'HEX', 'HEX', dimension='2D')

    location, band = FA.SearchBandExtremum(61,extremum='min')

    print(location)

    x = np.linspace(0,100,len(band))
    plt.plot(x,band)