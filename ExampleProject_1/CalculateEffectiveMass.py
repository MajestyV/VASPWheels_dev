import numpy as np
import matplotlib.pyplot as plt
from VaspWheels import GetKpath,GetElectronicBands
from scipy.optimize import leastsq

GK = GetKpath.vasp()             # 调用GetKpath模块
GEB = GetElectronicBands.vasp()  # 调用GetElectronicBands模块

##################################################################################################################
# 先定义一些在接下来的计算中可能用到的参数

# 晶体结构信息

crystal_info = ['HEX', [3.1473295667554400, 3.1473295667554400, 43.9122903625234997, 90, 90, 120], 'primitive']

real_lattice = [[3.1473295667554400, 0.0000000000000000, 0.0000000000000000],
                [-1.5736647833777198, 2.7256673589277995, 0.0000000000000000],
                [0.0000000000000000, 0.0000000000000000, 43.9122903625234997]]

reciprocal_lattice = GK.CalculateReciprocalLattice(real_lattice)

# 一些关键的高对称点（High symmetry point, HSP）
HSP = {'G':  [0, 0, 0],
       'M':  [1/2.0,0,0],
       'M1': [1/2.0,-1/2.0,0],
       'K':  [1/3.0, 1/3.0, 0],
       'Sl': [0.26500000000050006,0,0],
       'S1': [1/3.0, 0, 0],
       'S2': [2/3.0, 0, 0],
       'L':  [0.176666666667, 0.176666666667, 0]}

# 计算曲率时的取点方向
direction = ['K-G','K-M','K-S1','K-S2',
             'G-K','G-M','G-M1',
             'L-K','L-G','L-Sl']

##################################################################################################################
# 生成计算迁移率所需的K点文件

# Kpath_directory = 'D:/PhD_research/Data/Simulation/MoS2/CarrierTransport/4/EffectiveMass/Kpath/'  # 宿舍电脑
Kpath_directory = 'D:/Projects/PhaseTransistor/Data/Simulation/Conductivity/EffectiveMass/Kpath/'  # 办公室电脑

origin =      [HSP['K'], HSP['K'], HSP['K'], HSP['K'], HSP['G'], HSP['G'], HSP['G'], HSP['L'], HSP['L'], HSP['L']]
destination = [HSP['G'], HSP['M'], HSP['S1'],HSP['S2'],HSP['K'], HSP['M'], HSP['M1'],HSP['K'], HSP['G'], HSP['Sl']]

Kpoints_list = GK.GenerateKpath_segment(origin,destination,30,0.01,reciprocal_lattice)

GK.GenKPOINTS(Kpath_directory+'K-path_EffectiveMass',Kpoints_list)

##################################################################################################################
# 计算电子跟空穴的有效质量
data_directory = 'D:/Projects/PhaseTransistor/Data/Simulation/Conductivity/EffectiveMass/4/4_PositiveField_EffectiveMass/'  # 办公室电脑

E_field = ['0.025', '0.050', '0.075', '0.100', '0.125', '0.150', '0.175', '0.200', '0.225', '0.250', '0.275', '0.300']
E_test = '0.025'

# 检查数据
EIGENVAL = data_directory+E_test+'/'+'EIGENVAL'
valence_band, conduction_band = GEB.GetBandEdges(EIGENVAL)

k = np.array([i for i in range(len(valence_band))])

#plt.plot(k,valence_band)
#plt.plot(k,conduction_band)
#plt.xlim(0,29)
#plt.ylim(1.42,1.44)

# 用于计算有效质量的函数
def CalculateEffectiveMass(Kstep,band,num_segment):
    num_point_total = len(band)  # 能带总点数
    num_point_segment = int(len(band)/num_segment)  # 每段能带中包含的点数

    # 应注意，V.A.S.P.中计算能带默认的长度单位是Å，能量单位是eV
    # 为了方便计算，并将最后的计算结果以电子静止质量m_{e}表示，我们需要将上述单位转换为原子单位制
    # 在原子单位制中，长度单位为Bohr， 1 Bohr = 0.529177210903 Å, 1 Bohr^{-1} = 1.8897261246257702 Å^{-1}
    # 能量单位为Hartree， 1 eV = 0.0367493 Hartree
    Kstep = Kstep/1.8897261246257702
    band = 0.0367493*np.array(band)
    print(band)

    Kpath_segment = np.array([i*Kstep for i in range(num_point_segment)])  # 生成每一段衡量有效质量的能带的K空间路程
    band_segmented = [band[i:i+num_point_segment] for i in range(0,num_point_total,num_point_segment)]  # 将能带进行分段
    print(band_segmented)

    #coef_list = []
    #EM_list = []
    #for i in range(num_segment):
        #coef = np.polyfit(Kpath_segment,band_segmented[i],2)  # 利用polyfit对能带进行二次项拟合
        #coef_list.append(coef)
        #m_effective = 1/(2*coef[0])
        #EM_list.append(m_effective)

    def function(p, x):
        A, B, C = p
        # return A * x ** 2 + B * x + C
        return A*x**2+C

    def error(p, x, y):
        return function(p, x) - y

    coef_list = []
    for i in range(num_segment):
        coef = leastsq(error,np.array([1,1,1]),args=(Kpath_segment,band_segmented[i]))
        coef_list.append(coef)

    plt.plot(Kpath_segment,band_segmented[0])

    #m = 1 / (2 * para[0][0])  # 计算有效质量

    return coef_list

print(CalculateEffectiveMass(0.01,valence_band,10))
#print(CalculateEffectiveMass(0.01,valance_band,10)[0])
#print(CalculateEffectiveMass(0.01,valance_band,10)[1])


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