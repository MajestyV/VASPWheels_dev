import numpy as np

from VaspWheels import AnalyzeStructure
from VaspWheels import Visualization

AS = AnalysisStructure.structure()  # 晶体结构分析包
plot = Visualization.plot()  # 画图包

data_repository = 'D:/Projects/PhaseTransistor/Data/Simulation/Structure_under_Efield/2/2_D3BJ_OPTCELL/relaxed_structure_'

data_file = ['0.000','0.025','0.050','0.075','0.100','0.125','0.150','0.175','0.200','0.225','0.250','0.275','0.300',
             '0.325','0.350','0.375','0.400','0.425','0.450','0.475','0.500','0.525','0.550']

Efield = []
a_list = []
b_list = []
c_2_list = []
Bond_Mo_S_1 = []
Bond_Mo_S_2 = []
Bond_Mo_S_3 = []
Bond_Mo_S_4 = []
for n in data_file:
    Efield.append(float(n)*10)

    Sturc_info = AS.GetStructure(data_repository+n)
    lattice_vector = Sturc_info['lattice_vector']
    atom_pos = Sturc_info['atomic_position']
    natom = Sturc_info['num_atom']

    num_Mo = int(natom[0])
    num_S = int(natom[1])
    Mo_1 = atom_pos[0]
    Mo_2 = atom_pos[1]
    S_1 = atom_pos[2]
    S_2 = atom_pos[3]
    S_3 = atom_pos[4]
    S_4 = atom_pos[5]

    lattice_param = AS.LatticeParameter(lattice_vector)
    a, b, c, alpha, beta, gamma = lattice_param

    c_2 = AS.BondLength(Mo_1,Mo_2,lattice_vector)
    d_Mo1_S1 = AS.BondLength(Mo_1,S_1,lattice_vector)
    d_Mo1_S2 = AS.BondLength(Mo_1,S_2,lattice_vector)
    d_Mo1_S3 = AS.BondLength(Mo_1,S_3,lattice_vector)
    d_Mo1_S4 = AS.BondLength(Mo_1,S_4,lattice_vector)
    d_Mo2_S1 = AS.BondLength(Mo_2,S_1,lattice_vector)
    d_Mo2_S2 = AS.BondLength(Mo_2,S_2,lattice_vector)
    d_Mo2_S3 = AS.BondLength(Mo_2,S_3,lattice_vector)
    d_Mo2_S4 = AS.BondLength(Mo_2,S_4,lattice_vector)

    #print(a,b,c_2)
    #print(d_Mo1_S1,d_Mo1_S2,d_Mo1_S3,d_Mo1_S4)
    #print(d_Mo2_S1,d_Mo2_S2,d_Mo2_S3,d_Mo2_S4)

    a_list.append(a)
    b_list.append(b)
    c_2_list.append(c_2)
    Bond_Mo_S_1.append(d_Mo1_S4)
    Bond_Mo_S_2.append(d_Mo1_S1)
    Bond_Mo_S_3.append(d_Mo2_S2)
    Bond_Mo_S_4.append(d_Mo2_S3)

plot.GlobalSetting()  # 全局画图变量

#plot.Visulize(Efield,a_list)
#plot.Visulize(Efield,b_list)
#plot.Visulize(Efield,c_2_list)
plot.Visulize(Efield,Bond_Mo_S_1,curve='spline',marker='o',color=np.array([254,129,125])/255.0)
plot.Visulize(Efield,Bond_Mo_S_2,curve='spline',marker='s',color=np.array([254,129,125])/255.0)
plot.Visulize(Efield,Bond_Mo_S_3,curve='spline',marker='o',color=np.array([129,184,223])/255.0)
plot.Visulize(Efield,Bond_Mo_S_4,curve='spline',marker='s',color=np.array([129,184,223])/255.0)

plot.FigureSetting(legend='True',labels=['$Mo_1-S_1$ bond', '$Mo_1-S_2$ bond', '$Mo_2-S_3$ bond', '$Mo_2-S_4$ bond'],
                   xlabel='Electric field (V/nm)',ylabel='Bond length ($\AA$)',xlim=(0,5.5),ylim=(2.397,2.401))