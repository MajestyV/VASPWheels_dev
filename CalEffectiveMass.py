import numpy as np
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
HSP = {'GAMMA': [0, 0, 0], 'K': [1/3.0, 1/3.0, 0], 'SIGMA_1':[2/3.0, 0, 0], 'SIGMA_2': [1/3.0, 0, 0],
       'M': [0.500, 0, 0], 'LAMBDA': [0.176666666667, 0.176666666667, 0]}

# 计算曲率时的取点方向
direction = ['K to GAMMA', 'K to SIGMA_1', 'K to M', 'LAMBDA to GAMMA', 'LAMBDA to SIGMA_2', 'GAMMA to K']

# This part is important
part1 = GEM.Interpolation(HSP['K'],HSP['GAMMA'],reciprocal_lattice=reciprocal)
part2 = GEM.Interpolation(HSP['K'],HSP['SIGMA_1'],reciprocal_lattice=reciprocal)
part3 = GEM.Interpolation(HSP['K'],HSP['M'],reciprocal_lattice=reciprocal)
part4 = GEM.Interpolation(HSP['LAMBDA'],HSP['GAMMA'],reciprocal_lattice=reciprocal)
part5 = GEM.Interpolation(HSP['LAMBDA'],HSP['SIGMA_2'],reciprocal_lattice=reciprocal)
part6 = GEM.Interpolation(HSP['GAMMA'],HSP['K'],reciprocal_lattice=reciprocal)
total = part1+part2+part3+part4+part5+part6

# 这个函数可以将GSE计算的有效质量数据写入excel文件
def ExportEffectiveMassData(saving_directory,data,Kpoint,Efield,filename='EffectiveMass'):
    workbook = xlwt.Workbook()

    sheet = workbook.add_sheet('ElectronEffectiveMass', cell_overwrite_ok=True)
    for i in range(len(Efield)):
        sheet.write(i + 1, 0, Efield[i])
        for j in range(len(Kpoint)):
            sheet.write(0, j + 1, Kpoint[j])
            sheet.write(i + 1, j + 1, data[i][j])
    workbook.save(saving_directory+filename+'.xls')
    return

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

        m_h, para_h = GEM.CalEffectiveMass(k,E_vb)  # 调用函数计算空穴有效质量
        m_e, para_e = GEM.CalEffectiveMass(k,E_cb)  # 调用函数计算电子有效质量

        m_hole.append(m_h)
        m_electron.append(m_e)

    m_hole_total.append(m_hole)
    m_electron_total.append(m_electron)

print(m_hole_total)
print(m_electron_total)

#workbook = xlwt.Workbook()

#sheet = workbook.add_sheet('ElectronEffectiveMass', cell_overwrite_ok=True)
#for i in range(len(E_field)):
    #sheet.write(i+1,0,E_field[i])
    #for j in range(len(direction)):
        #sheet.write(0,j+1,direction[j])
        #sheet.write(i+1,j+1,m_electron_total[i][j])
#workbook.save(data_repository+'EffectiveMass.xls')

ExportEffectiveMassData(data_repository,m_electron_total,direction,E_field,filename='EM_electron')
ExportEffectiveMassData(data_repository,m_hole_total,direction,E_field,filename='EM_hole')