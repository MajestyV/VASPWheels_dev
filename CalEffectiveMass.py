import os

import numpy as np
import xlrd
import xlwt
import matplotlib.pyplot as plt
from VaspWheels import Crystallography
from VaspWheels import GetEffectiveMass

crystal = Crystallography.Crystal()
GEM = GetEffectiveMass.EffectiveMass()

lattice = ['HEX', [3.1473295667554400, 3.1473295667554400, 43.9122903625234997, 90, 90, 120], 'primitive']
crystal_class, lattice_para, cell_type = lattice
reciprocal = crystal.Reciprocal_lattice(crystal_class,lattice_para)

data_repository = 'D:/Projects/PhaseTransistor/Data/Simulation/Conductivity/Mobility/4/EffectiveMass/4_GSE_EffectiveMass/'

E_field = ['0.025', '0.050', '0.075', '0.100', '0.125', '0.150', '0.175', '0.200', '0.225', '0.250', '0.275', '0.300']
E_test = ['0.025']

# HSP = High Symmetry Point （高对称点）
HSP = {'Gamma': [0, 0, 0], 'K': [1/3.0, 1/3.0, 0], 'Lambda':[2/3.0, 0, 0],
       'M': [0.500, 0, 0], 'Sigma': [0.176666666667, 0.176666666667, 0], 'Alpha': [1/3.0, 0, 0]}

direction = ['K to Gamma', 'K to Lambda', 'K to M', 'Sigma to Gamma', 'Sigma to Alpha', 'Gamma to K']

# This part is important
part1 = GEM.Interpolation(HSP['K'],HSP['Gamma'],reciprocal_lattice=reciprocal)
part2 = GEM.Interpolation(HSP['K'],HSP['Lambda'],reciprocal_lattice=reciprocal)
part3 = GEM.Interpolation(HSP['K'],HSP['M'],reciprocal_lattice=reciprocal)
part4 = GEM.Interpolation(HSP['Sigma'],HSP['Gamma'],reciprocal_lattice=reciprocal)
part5 = GEM.Interpolation(HSP['Sigma'],HSP['Alpha'],reciprocal_lattice=reciprocal)
part6 = GEM.Interpolation(HSP['Gamma'],HSP['K'],reciprocal_lattice=reciprocal)
total = part1+part2+part3+part4+part5+part6



def function(p, x):
    A, B, C = p
    return A * x ** 2 + B * x + C

m_hole_total = []
m_electron_total = []
for n in E_field:
    EIGENVAL = data_repository+n+'/'+'EIGENVAL'
    k_point, vb, cb = GEM.GetBandEdge(EIGENVAL, 96, 97)   # 将特定电场下的能带数据提取出来

    m_hole = []
    m_electron = []

    for i in range(6):  # 6 K-point in the K-space is evaluated
        k = []
        E_vb = []
        E_cb = []
        for j in range(6):  # 每个K点附近都插值了6个点用于多项式拟合计算有效质量
            origin = 6*i
            length = GEM.Length(k_point[origin],k_point[origin+j],reciprocal)
            k.append(length)
            E_vb.append(np.array(vb[origin+j]))
            E_cb.append(np.array(cb[origin+j]))

        k = np.array(k)  # 将k从list转换为array方便后面计算

        m_h, para_h = GEM.CalEffectiveMass(k,E_vb)  # 调用函数计算有效质量
        m_e, para_e = GEM.CalEffectiveMass(k,E_cb)

        m_hole.append(m_h)
        m_electron.append(m_e)

    m_hole_total.append(m_hole)
    m_electron_total.append(m_electron)

print(m_hole_total)
print(m_electron_total)

# os.remove(data_repository+'EffectiveMass.xls')

# workbook = xlrd.open_workbook(data_repository+'EffectiveMass.xls')
workbook = xlwt.Workbook()
cell_overwrite_ok=True

sheet = workbook.add_sheet('ElectronEffectiveMass')
for i in range(len(E_field)):
    sheet.write(i+2,1,E_field[i])
    for j in range(len(direction)):
        sheet.write(1,j+2,direction[j])
        sheet.write(i+2,j+2,m_electron_total[i][j])
workbook.save(data_repository+'EffectiveMass.xls')


#x = np.linspace(0,0.008,100)

#plt.plot(k/1.8897261246257702,0.0367493*np.array(vb_k))
#plt.plot(x,function(para,x))

#print(para)
#print(m)