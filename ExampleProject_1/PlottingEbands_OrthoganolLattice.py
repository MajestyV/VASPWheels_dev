import codecs
import re
from VaspWheels import GetKpath
from VaspWheels import GetElectronicBands
from VaspWheels import VisualizeBands


GK = GetKpath.Kpath()           # 调用GetKpath模块
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

# K点路径
Kpath_dict = {'ORT': [[r'$\Gamma$', 'X', 'S', 'Y', r'$\Gamma$', 'S'],
                     [[0, 0, 0], [0.5, 0, 0], [0.5, 0.5, 0], [0, 0.5, 0], [0, 0, 0], [0.5, 0.5, 0]]],
              'ORT_1': [[r'$\Gamma$', 'Y', 'S', 'X', r'$\Gamma$', 'S'],
                       [[0, 0, 0], [0, 0.5, 0], [0.5, 0.5, 0], [0.5, 0, 0], [0, 0, 0], [0.5, 0.5, 0]]],
              '2D': [[r'$\Gamma$', 'M', 'K', r'$\Gamma$'],
                   [[0, 0, 0], [0.5, 0, 0], [1.0 / 3.0, 1.0 / 3.0, 0], [0, 0, 0]]],
              '3D': [[r'$\Gamma$','M', 'K', r'$\Gamma$', 'A', 'L', 'H', 'A'],
                   [[0, 0, 0], [0.5, 0, 0], [1.0 / 3.0, 1.0 / 3.0, 0], [0, 0, 0], [0,0,1/2.0], [1/2.0,0,1/2.0], [1/3.0, 1/3.0, 1/2.0], [0,0,1/2.0]]]}
# Kpath = Kpath_dict['ORT_1']  # Plotting the bands along 2D K_path

lattice = ['ORT', [3.16, 5.47, 12.9, 90, 90, 90], 'unitcell']

# 生成投影到一维的K点路径
num_segments = 5
Kpath_projected,Knodes_projected = GK.ProjectKpath(Kpath,num_segments,LatticeCorrection='True',Lattice=lattice)
# print(Kpath_projected)
# print(Knodes_projected)

# 费米面调零
Markdown = data_directory+result[1]+'/Markdown_SCF'  # 这个文件记载着准确的费米能级
pattern = re.compile(r'-?\d+\.?\d+')  # 匹配浮点数的正则表达式
f = codecs.open(Markdown, 'rb', 'utf-8', 'ignore')
line = f.readline()
Energy = pattern.findall(line)
#print(Energy)
Efermi = float(Energy[0])
#value = line.split()
#value = list(map(float,value))
#print(Energy)
#print(Efermi)

bands_shifted = GE.ShiftFermiSurface(bands,Efermi-0.34)

VB.Electron_bands(Kpath_projected,bands_shifted,Knodes_projected,ylim=(-2,4.5))