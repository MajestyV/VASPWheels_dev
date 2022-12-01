from VaspWheels import AnalyzeBandgap
from VaspWheels import VisualizeEbands

AB = AnalyzeBandgap.Bandgap()  # 调用AnalyzeBandgap模块
VB = VisualizeEbands.Ebands()  # 调用VisualizeEbands模块

####################################################################################################################
# 数据文件夹的地址的导入

# 储存存放数据的文件夹的绝对地址的字典
# Main_directory = 'D:/Projects/PhaseTransistor/Data/Simulation/GSE/1/1_D3BJ_GSE_1_221013/'
Main_directory = 'D:/Projects/PhaseTransistor/Data/Simulation/GSE/4/4_D3BJ_GSE_1_more_bands'
# Main_directory = 'D:/Projects/PhaseTransistor/Data/Simulation/GSE/5/5_D3BJ_GSE_1/'

Efield = '0.200'  # 在特定结构子文件夹中，存放数据的文件夹；同时也恰好时电场强度，单位为V/Angstrom

data_directory = Main_directory+'/'+Efield+'/'  # 存放画能带图所需的数据文件的绝对地址

EIGENVAL = data_directory+'/EIGENVAL'  # EIGENVAL文件的绝对地址

####################################################################################################################
# 获取K空间高对称点路径

# K_path
K_path = {'2D': [[r'$\Gamma$', 'M', 'K', r'$\Gamma$'],
                 [[0, 0, 0], [0.5, 0, 0], [1.0 / 3.0, 1.0 / 3.0, 0], [0, 0, 0]]],
          '3D': [[r'$\Gamma$','M', 'K', r'$\Gamma$', 'A', 'L', 'H', 'A'],
                 [[0, 0, 0], [0.5, 0, 0], [1.0 / 3.0, 1.0 / 3.0, 0], [0, 0, 0], [0,0,1/2.0], [1/2.0,0,1/2.0], [1/3.0, 1/3.0, 1/2.0], [0,0,1/2.0]]]}
# Kpoints = [r'$\Gamma$','M', 'K', r'$\Gamma$', 'A', 'L', 'H', 'A']
# path = [[0, 0, 0], [0.5, 0, 0], [1.0 / 3.0, 1.0 / 3.0, 0], [0, 0, 0], [0,0,1/2.0], [1/2.0,0,1/2.0], [1/3.0, 1/3.0, 1/2.0], [0,0,1/2.0]]
#Kpoints = [r'$\Gamma$', 'M', 'K', r'$\Gamma$']
#path = [[0, 0, 0], [0.5, 0, 0], [1.0 / 3.0, 1.0 / 3.0, 0], [0, 0, 0]]
Kpoints = K_path['2D']  # Plotting the bands along 2D K_path

lattice = ['HEX', [3.16, 3.16, 12.9, 90, 90, 120], 'primitive']  # The parameters of hexagonal lattice

###################################################################################################################
# 选取费米能级

# 采用静态自洽场（SCF）计算得到的费米能级
#Markdown = data_directory+'/Markdown_SCF'  # 这个文件记载着准确的费米能级
#pattern = re.compile(r'-?\d+\.?\d+')  # 匹配浮点数的正则表达式
#f = codecs.open(Markdown, 'rb', 'utf-8', 'ignore')
#line = f.readline()
#Energy = pattern.findall(line)
#Efermi = float(Energy[0])

# 将费米能级调整到价带顶
valence, conduction = AB.AnalyzeOccupation(EIGENVAL)
Efermi = max(valence)  # 价带顶即为费米面（后面的系数是线宽修正）

###############################################################################################################
# 可视化

title = r'$\mathcal{E}$ = 1.00 V/nm'  # 标题

VB.Ebands(EIGENVAL,Kpoints[1],LatticeCorrection='True',Lattice=lattice,ShiftFermi='True',Efermi=Efermi,
          Kpoints=Kpoints[0],ylim=(-3,5),title=title,latex='False')