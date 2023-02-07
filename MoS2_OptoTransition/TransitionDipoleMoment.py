########################################################################################################################
# 模块调用
from VaspWheels import GetKpath,GetElectronicBands,Visualization,VisualizeBands

GK = GetKpath.vasp()              # 调用GetKpath模块（可以获取K点路径）
GE = GetElectronicBands.vasp()    # 调用GetElectronicBands模块（可以获取能带数据）
VI = Visualization.plot()         # 调用Visualization模块（可视化基础包）
VB = VisualizeBands.plot_bands()  # 调用VisualizeBands模块（能带可视化专用包）

########################################################################################################################
# 导入V.A.S.P.计算结果文件
# 计算结果的存放总目录
data_directory = 'D:/Projects/OptoTransition/Data/MoS2_ElectronicStructure'  # 办公室电脑

# 以字典的形式记录的子目录
sub_dir_dict = {'Bulk': ['bulk_CrudeRelax','bulk_FineRelax']}  # 键指代子目录，值中的列表列出子目录下所有构型计算所得的结果
sub_dir = 'Bulk'  # 子目录引索，用于指定要分析的数据所在子目录
index = 0         # 子目录下的数据文件夹中的引索，与sub_dir_dict中的值中的列表对应

EIGENVAL = data_directory+'/'+sub_dir+'/'+sub_dir_dict[sub_dir][index]+'/EIGENVAL'  # 能带计算结果（EIGENVAL）的绝对地址

########################################################################################################################
# 分析整理能带计算结果
bands_dict = GE.GetEbands(EIGENVAL)      # 提取能带计算结果以及各种参数
num_bands = bands_dict['num_bands']      # 提取能带总数
num_kpoints = bands_dict['num_kpoints']  # 提取K点总数
Kpath = bands_dict['Kpath']  # K点路径
bands = bands_dict['bands']  # 能带具体的能量值

# 高对称点名称
HighSymPoint_dict = {'ORT': [r'$\Gamma$', 'X', 'S', 'Y', r'$\Gamma$', 'S'],
                     'ORT_1': [r'$\Gamma$', 'Y', 'S', 'X', r'$\Gamma$', 'S'],
                     'ORT_2': [r'$\Gamma$', 'X', 'S', r'$\Gamma$', 'Y'],
                     'HEX_2D': [r'$\Gamma$', 'M', 'K', r'$\Gamma$'],
                     'HEX_3D': [r'$\Gamma$','M', 'K', r'$\Gamma$', 'A', 'L', 'H', 'A']}

lattice = ['ORT', [3.16, 5.47, 12.9, 90, 90, 90], 'unitcell']

# 生成投影到一维的K点路径
num_segments = 7
Kpath_projected,Knodes_projected = GK.ProjectKpath(Kpath,num_segments,LatticeCorrection='True',Lattice=lattice)
# print(Kpath_projected)
# print(Knodes_projected)

# 费米面调零
Eg, Ev_max, Ec_min, extremum_location = GE.GetBandgap(EIGENVAL,mode='occupation')

bands_shifted = GE.ShiftFermiSurface(bands,Ev_max)

VB.Electron_bands(Kpath_projected,bands_shifted,Knodes_projected,ylim=(-2.2,4.5),HighSymPoint=HighSymPoint_dict['HEX_3D'])

#plt.vlines(0.9941748903765186*(2.0/3.0),-2.2,4.5, linewidth=2, linestyles='dashed',colors=VI.MorandiColor('Black'))
#plt.text(0.5,0.1,'K',size=16)

# 数据保存
# saving_directory = 'D:/Projects/PhaseTransistor/Data/Figures/CarrierTransportation/'  # 办公室电脑
#saving_directory = 'D:\PhD_research\Gallery\Carrier transportation\Orthogonal supercell/'  # 宿舍电脑
#VI.SavingFigure(saving_directory,filename='Ebands_OrtCell_Manual',format='pdf')