import codecs
import re
from VaspWheels import GetBandEdge
from VaspWheels import VisualizeEbands

GBE = GetBandEdge.BandEdge()   # 导带，价带以及费米面数据提取模块
VB = VisualizeEbands.Ebands()  # 能带可视化专用模块

Data = {'LDA':'/Users/liusongwei/MaterialsGallery/MoS2/Data/MoS2_2H/MoS2_pawlda_SOC/',  # Data for xc-function LDA
        'PBE':'D:/Projects/PhaseTransistor/Data/Simulation/MoS2_pawpbe_vasp5_D3BJ/',  # Data for xc-function PBE
        'GSE':'D:/Projects/PhaseTransistor/Data/Simulation/GSE/'}            # Data for GSE calculation
Repository = Data['PBE']  # 选择可视化PBE关联函数的计算结果

# 指定特定的结构
nlayer = 'Bulk'
directory = 'result_OPTCELL_SOC'
# title = r'Band structure of '+nlayer+' $MoS_2$'
title = r''

# Address of the data file
EIGENVAL = Repository+nlayer+'/'+directory+'/EIGENVAL'

# K_path
K_path = {'2D': [[r'$\Gamma$', 'M', 'K', r'$\Gamma$'],
                 [[0, 0, 0], [0.5, 0, 0], [1.0 / 3.0, 1.0 / 3.0, 0], [0, 0, 0]]],
          '3D': [[r'$\Gamma$','M', 'K', r'$\Gamma$', 'A', 'L', 'H', 'A'],
                 [[0, 0, 0], [0.5, 0, 0], [1.0 / 3.0, 1.0 / 3.0, 0], [0, 0, 0], [0,0,1/2.0], [1/2.0,0,1/2.0], [1/3.0, 1/3.0, 1/2.0], [0,0,1/2.0]]]}
# Kpoints = [r'$\Gamma$','M', 'K', r'$\Gamma$', 'A', 'L', 'H', 'A']
# path = [[0, 0, 0], [0.5, 0, 0], [1.0 / 3.0, 1.0 / 3.0, 0], [0, 0, 0], [0,0,1/2.0], [1/2.0,0,1/2.0], [1/3.0, 1/3.0, 1/2.0], [0,0,1/2.0]]
#Kpoints = [r'$\Gamma$', 'M', 'K', r'$\Gamma$']
#path = [[0, 0, 0], [0.5, 0, 0], [1.0 / 3.0, 1.0 / 3.0, 0], [0, 0, 0]]
Kpoints = K_path['3D']  # Plotting the bands along 2D K_path

lattice = ['HEX', [3.16, 3.16, 12.9, 90, 90, 120], 'primitive']  # The parameters of hexagonal lattice


#Markdown = Repository+nlayer+'/'+directory+'/Markdown_SCF'  # 这个文件记载着准确的费米能级
#pattern = re.compile(r'-?\d+\.?\d+')  # 匹配浮点数的正则表达式
#f = codecs.open(Markdown, 'rb', 'utf-8', 'ignore')
#line = f.readline()
#Energy = pattern.findall(line)
#Efermi = float(Energy[0])

valence, conduction = GBE.GetBandEdge(EIGENVAL)
Efermi = max(valence)+0.05  # 价带顶即为费米面（后面的系数是线宽修正）

VB.Ebands(EIGENVAL,Kpoints[1],LatticeCorrection='True',Lattice=lattice,ShiftFermi='True',Efermi=Efermi,
          Kpoints=Kpoints[0],ylim=(-3,5),title=title,latex='False')