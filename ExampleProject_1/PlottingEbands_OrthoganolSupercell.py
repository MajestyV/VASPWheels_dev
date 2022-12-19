import matplotlib.pyplot as plt

from VaspWheels import GetKpath,GetElectronicBands,Visualization,VisualizeBands

GK = GetKpath.vasp()              # 调用GetKpath模块
GE = GetElectronicBands.vasp()    # 调用GetElectronicBands模块
VI = Visualization.plot()         # 调用Visualization模块
VB = VisualizeBands.plot_bands()  # 调用VisualizeBands模块（能带可视化专用包）

################################################################################################################
# 第一性原理计算结果的存放目录
# data_directory = 'D:/Projects/PhaseTransistor/Data/Simulation/CarrierTransport/4/Ort_supercell/Ebands/2H_quadrilayer_ManualOptimized/'  # 办公室电脑
data_directory = 'D:/PhD_research/Data/Simulation/MoS2/CarrierTransport/4/Ort_supercell/Ebands/2H_quadrilayer_ManualOptimized/'  # 宿舍电脑
# data_directory = 'D:/PhD_research/Data/Simulation/MoS2/CarrierTransport/4/Ort_supercell/Ebands/2H_quadrilayer_14_8_1_shifted/'  # 宿舍电脑-VASP优化原胞

result = ['result_D3BJ_SOC_OrtCell', 'result_D3BJ_SOC_DifferentPath']

filename = 'EIGENVAL'

# 能带计算结果（EIGENVAL）的绝对地址
EIGENVAL = data_directory+result[0]+'/'+filename
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
num_segments = 4
Kpath_projected,Knodes_projected = GK.ProjectKpath(Kpath,num_segments,LatticeCorrection='True',Lattice=lattice)
# print(Kpath_projected)
# print(Knodes_projected)

# 费米面调零
Eg, Ev_max, Ec_min, extremum_location = GE.GetBandgap(EIGENVAL,mode='occupation')

bands_shifted = GE.ShiftFermiSurface(bands,Ev_max)

VB.Electron_bands(Kpath_projected,bands_shifted,Knodes_projected,ylim=(-2.2,4.5),HighSymPoint=HighSymPoint_dict['ORT_2'])

plt.vlines(0.9941748903765186*(2.0/3.0),-2.2,4.5, linewidth=2, linestyles='dashed',colors=VI.MorandiColor('Black'))
plt.text(0.5,0.1,'K',size=16)

# 数据保存
# saving_directory = 'D:/Projects/PhaseTransistor/Data/Figures/CarrierTransportation/'  # 办公室电脑
saving_directory = 'D:\PhD_research\Gallery\Carrier transportation\Orthogonal supercell/'  # 宿舍电脑
VI.SavingFigure(saving_directory,filename='Ebands_OrtCell_Manual',format='pdf')