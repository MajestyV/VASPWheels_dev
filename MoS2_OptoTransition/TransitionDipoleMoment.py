########################################################################################################################
# 模块调用
from VaspWheels import GetKpath,GetElectronicBands,Visualization,VisualizeBands

GK = GetKpath.vasp()              # 调用GetKpath模块（可以获取K点路径）
GE = GetElectronicBands.vasp()    # 调用GetElectronicBands模块（可以获取能带数据）
VI = Visualization.plot()         # 调用Visualization模块（可视化基础包）
VB = VisualizeBands.plot_bands()  # 调用VisualizeBands模块（能带可视化专用包）

########################################################################################################################
# 程序输入（通过改变这一部分的变量，我们可以调整程序的运行结果，更细致地说，此部分代码决定了程序的总输入，我们可以在这控制我们想画的曲线及样式）
working_station = 'C221'  # 工作地点，选项有Office, C221, 以及Macbook
target_data = ('Bulk',0)  # (子目录名称,子目录下的数据文件夹名称在sub_dir_dict中的引索)
bands_setting = ('HEX','HEX_3D')  # (crystal lattice, high symmetry point (HSP) path)
saving_filename = 'Bulk_MoS2'  # 数据文件保存时的名称

########################################################################################################################
# 导入V.A.S.P.计算结果文件
# 计算结果的存放主目录 # 办公室电脑
main_dir_dict = {'Office': 'D:/Projects/OptoTransition/Data/MoS2_ElectronicStructure',  # 办公室电脑
                 'C221': 'D:/Projects/OptoTransition/Data/MoS2_ElectronicStructure'}    # 宿舍电脑

# 以字典的形式记录的子目录
sub_dir_dict = {'Bulk': ['bulk_CrudeRelax','bulk_FineRelax']}  # 键指代子目录，值中的列表列出子目录下所有构型计算所得的结果
sub_dir, data_dir_index = target_data  # 从target_data中解压出子目录名称以及子目录下的数据文件夹的引索

# 能带计算结果（EIGENVAL）的绝对地址
EIGENVAL = main_dir_dict[working_station]+'/'+sub_dir+'/'+sub_dir_dict[sub_dir][data_dir_index]+'/EIGENVAL'

########################################################################################################################
# 分析整理能带计算结果
bands_dict = GE.GetEbands(EIGENVAL)      # 提取能带计算结果以及各种参数
num_bands = bands_dict['num_bands']      # 提取能带总数
num_kpoints = bands_dict['num_kpoints']  # 提取K点总数
Kpath = bands_dict['Kpath']  # K点路径
bands = bands_dict['bands']  # 能带具体的能量值

# 存放晶体结构参数的字典
lattice_dict = {'HEX': ['HEX', [3.16, 3.16, 12.9, 90, 90, 120], 'primitive'],
                'ORT': ['ORT', [3.16, 5.47, 12.9, 90, 90, 90], 'unitcell']}

# 存放高对称点路径的字典
HighSymPoint_dict = {'HEX_2D': [r'$\Gamma$', 'M', 'K', r'$\Gamma$'],
                     'HEX_3D': [r'$\Gamma$','M', 'K', r'$\Gamma$', 'A', 'L', 'H', 'A'],
                     'ORT': [r'$\Gamma$', 'X', 'S', 'Y', r'$\Gamma$', 'S'],
                     'ORT_1': [r'$\Gamma$', 'Y', 'S', 'X', r'$\Gamma$', 'S'],
                     'ORT_2': [r'$\Gamma$', 'X', 'S', r'$\Gamma$', 'Y']}

lattice, HSP = bands_setting  # 从bands_setting中解压出画能带所需的结构参数

# 生成投影到一维的K点路径
num_segments = 7
Kpath_projected,Knodes_projected = GK.ProjectKpath(Kpath,num_segments,LatticeCorrection='True',Lattice=lattice_dict[lattice])
# print(Kpath_projected)
# print(Knodes_projected)

########################################################################################################################
# 绘制能带图

Eg, Ev_max, Ec_min, extremum_location = GE.GetBandgap(EIGENVAL,mode='occupation')  # 寻找价带顶跟导带底以及计算带隙
bands_shifted = GE.ShiftFermiSurface(bands,Ev_max)  # 费米面调零

VB.Electron_bands(Kpath_projected,bands_shifted,Knodes_projected,ylim=(-2,5),y_major_tick=1,
                  HighSymPoint=HighSymPoint_dict[HSP])

#plt.vlines(0.9941748903765186*(2.0/3.0),-2.2,4.5, linewidth=2, linestyles='dashed',colors=VI.MorandiColor('Black'))
#plt.text(0.5,0.1,'K',size=16)

# 数据保存
saving_dir_dict = {'Office': 'D:/Projects/OptoTransition/Data/MoS2_ElectronicStructure',  # 办公室电脑
                   'C221': 'D:/Projects/OptoTransition/Data/Figures/Band structure'}    # 宿舍电脑
VI.SavingFigure(saving_dir_dict[working_station]+'/',filename=saving_filename,format='eps')
VI.SavingFigure(saving_dir_dict[working_station]+'/',filename=saving_filename,format='pdf')
VI.SavingFigure(saving_dir_dict[working_station]+'/',filename=saving_filename,format='png')