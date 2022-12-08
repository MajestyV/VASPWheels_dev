import codecs
import re
from VaspWheels import GetKpath
from VaspWheels import GetElectronicBands
from VaspWheels import VisualizeBands


GK = GetKpath.vasp()           # 调用GetKpath模块
GE = GetElectronicBands.vasp()  # 调用GetElectronicBands模块
VB = VisualizeBands.plotting()  # 调用VisualizeBands模块（能带可视化专用包）

################################################################################################################
# 第一性原理计算结果的存放目录
data_directory = 'D:/Projects/PhaseTransistor/Data/Simulation/Conductivity/Orthogonal_supercell/4/'

result = ['result_D3BJ/', 'result_D3BJ_SOC/']

filename = 'EIGENVAL'

# 能带计算结果（EIGENVAL）的绝对地址
EIGENVAL = data_directory+result[1]+filename
###################################################################################################################
# 数据提取与整理
# 提取能带计算结果以及各种参数
bands_dict = GE.GetEbands(EIGENVAL)
num_bands = bands_dict['num_bands']      # 提取能带总数
num_kpoints = bands_dict['num_kpoints']  # 提取K点总数
Kpath = bands_dict['Kpath']  # K点路径
bands = bands_dict['bands']  # 能带具体的能量值

# 高对称点名称
HighSymPoint_dict = {'ORT': [r'$\Gamma$', 'X', 'S', 'Y', r'$\Gamma$', 'S'],
                     'ORT_1': [r'$\Gamma$', 'Y', 'S', 'X', r'$\Gamma$', 'S'],
                     'ORT_2': [r'$\Gamma$', 'X', 'S', r'$\Gamma$', 'Y'],
                     '2D_HEX': [r'$\Gamma$', 'M', 'K', r'$\Gamma$'],
                     '3D_HEX': [r'$\Gamma$','M', 'K', r'$\Gamma$', 'A', 'L', 'H', 'A']}

lattice = ['ORT', [3.16, 5.47, 12.9, 90, 90, 90], 'unitcell']

# 生成投影到一维的K点路径
num_segments = 5
Kpath_projected,Knodes_projected = GK.ProjectKpath(Kpath,num_segments,LatticeCorrection='True',Lattice=lattice)
# print(Kpath_projected)
# print(Knodes_projected)

# 费米面调零
Eg, Ev_max, Ec_min, extremum_location = GE.GetBandgap(EIGENVAL,mode='occupation')

bands_shifted = GE.ShiftFermiSurface(bands,Ev_max)

VB.Electron_bands(Kpath_projected,bands_shifted,Knodes_projected,ylim=(-2,4.5),HighSymPoint=HighSymPoint_dict['ORT_1'])