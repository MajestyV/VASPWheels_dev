import codecs
import re
from VaspWheels import VisualizeEbands

VB = VisualizeEbands.Plotting()  # 能带可视化专用包

Data = {'LDA':'D:/MaterialsGallery/Testing/MoS2_pawlda/MoS2_2H/',  # Data for xc-function LDA
        'PBE':'D:/MaterialsGallery/Testing/MoS2_pawpbe/MoS2_2H/'}  # Data for xc-function PBE
Repository = Data['PBE']  # 选择可视化PBE关联函数的计算结果

# 指定特定的结构
nlayer = '2'
# title = r'Band structure of '+nlayer+' $MoS_2$'
title = r'ISIF = 4 without DFT-D2 correction'

# Address of the data file
EIGENVAL = Repository+nlayer+'/result_noD2_ISIF4/EIGENVAL'

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


Markdown = Repository+nlayer+'/result_noD2_ISIF4/Markdown_SCF'  # 这个文件记载着准确的费米能级
pattern = re.compile(r'-?\d+\.?\d+')  # 匹配浮点数的正则表达式
f = codecs.open(Markdown, 'rb', 'utf-8', 'ignore')
line = f.readline()
Energy = pattern.findall(line)
Efermi = float(Energy[0])
#value = line.split()
#value = list(map(float,value))
#print(Energy)
print(Efermi)



a = VB.Ebands(EIGENVAL,Kpoints[1],LatticeCorrection='True',Lattice=lattice,ShiftFermi='True',Efermi=-1.35778,Kpoints=Kpoints[0],ylim=(-3,5),title=title,latex='False')
# print(len(a['energy'][0]))
# print(len(a['occupation'][31]))
# print(a[1])
# kpath.GetKpath(saving_directory,path,59)