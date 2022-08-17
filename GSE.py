import re
import codecs
import numpy as np
import scipy.stats as st
import matplotlib.pyplot as plt
from VaspWheels import GetBandEdge

GBE = GetBandEdge.BandEdge()

home_dir_2_1 = 'D:/Projects/PhaseTransistor/Data/Simulation/GSE/2/2_D3BJ_GSE_1'
home_dir_2_m1 = 'D:/Projects/PhaseTransistor/Data/Simulation/GSE/2/2_D3BJ_GSE_m1'
home_dir_2_standard = 'D:/Projects/PhaseTransistor/Data/Simulation/GSE/2/Bilayer_standard'
home_dir_3_1 = 'D:/Projects/PhaseTransistor/Data/Simulation/GSE/3/3_D3BJ_GSE_1'
home_dir_3_m1 = 'D:/Projects/PhaseTransistor/Data/Simulation/GSE/3/3_D3BJ_GSE_m1'
home_dir_4_1 = 'D:/Projects/PhaseTransistor/Data/Simulation/GSE/4/4_D3BJ_GSE_1_more_bands'
home_dir_4_m1 = 'D:/Projects/PhaseTransistor/Data/Simulation/GSE/4/4_D3BJ_GSE_m1_more_bands'
home_dir_5_1 = 'D:/Projects/PhaseTransistor/Data/Simulation/GSE/5/5_D3BJ_GSE_1'
home_dir_5_m1 = 'D:/Projects/PhaseTransistor/Data/Simulation/GSE/5/5_D3BJ_GSE_m1'
home_dir_6_1 = 'D:/Projects/PhaseTransistor/Data/Simulation/GSE/Non-SOC/2/2_D3BJ_GSE_1'
# home_dir_4 = 'H:/Raw_Data/GSE_pawpbe_SOC_MoS2/2_D3BJ_GSE_1'
Data_point_0 = ['0.025','0.050','0.075','0.100','0.125','0.150','0.175','0.200','0.225','0.250','0.275','0.300',
                '0.325','0.350','0.375','0.400','0.425','0.450','0.475','0.500','0.525','0.550']
Data_point_1 = ['0.000','0.025','0.050','0.075','0.100','0.125','0.150','0.175','0.200','0.225','0.250','0.275','0.300',
                '0.325','0.350','0.375','0.400','0.425','0.450','0.475','0.500','0.525','0.550']
Data_point_2 = ['m0.550','m0.525','m0.500','m0.475','m0.450','m0.425','m0.400','m0.375','m0.350','m0.325','m0.300','m0.275',
                'm0.250','m0.225','m0.200','m0.175','m0.150','m0.125','m0.100','m0.075','m0.050','m0.025']
# Data_point_2 = ['0.000','0.010','0.020','0.030','0.040','0.050','0.060','0.070','0.080','0.090',
                # '0.100','0.110','0.120','0.130','0.140','0.150','0.160','0.170','0.180','0.190',
                # '0.200','0.210','0.220','0.230','0.240','0.250','0.260','0.270','0.280','0.290',
                # '0.300','0.310','0.320','0.330','0.340','0.350','0.360','0.370','0.380','0.390',
                # '0.400','0.410','0.420','0.430','0.440','0.450','0.460','0.470','0.480','0.490',
                # '0.500']
# 0.320
Data_point_3 = ['0.000','0.025','0.050','0.075','0.100','0.125','0.150','0.175','0.200','0.225','0.250','0.275','0.300']
#Data_point_4 = ['m0.025','m0.050','m0.075','m0.100','m0.125','m0.150','m0.175','m0.200','m0.225','m0.250','m0.275','m0.300']
Data_point_4 = ['m0.300','m0.275','m0.250','m0.225','m0.200','m0.175','m0.150','m0.125','m0.100','m0.075','m0.050','m0.025']

Data_point_5 = ['0.000','0.025','0.050','0.075','0.100','0.125','0.150','0.175','0.200','0.225','0.250']
#Data_point_4 = ['m0.025','m0.050','m0.075','m0.100','m0.125','m0.150','m0.175','m0.200','m0.225','m0.250','m0.275','m0.300']
Data_point_6 = ['m0.250','m0.225','m0.200','m0.175','m0.150','m0.125','m0.100','m0.075','m0.050','m0.025']

def Check_GSE_Data(data_point,home_directory,file_list=('output_SCF','output_DOS','output_Ebands')):
    beacon = '   1 F= '  # 计算正常进行的标志
    result = np.zeros((len(data_point),len(file_list)))
    for i in data_point:
        for j in file_list:
            log_file = home_directory+'/'+i+'/result/'+j  # 日志文件的地址
            f = codecs.open(log_file,'rb','utf-8','ignore')
            line = f.readline()
            indicator = 0  # 复位
            while line:
                if re.match(beacon,line) != None:
                    indicator += 1
                else:
                    pass
                line = f.readline()
            f.close()
            result[data_point.index(i),file_list.index(j)] = indicator
    return result

def Extract_Fermi_energy(data_point,home_directory):
    E_fermi = []
    for n in data_point:
        Markdown = home_directory + '/' + n + '/Markdown_SCF'  # 这个文件记载着准确的费米能级
        pattern = re.compile(r'-?\d+\.?\d+')  # 匹配浮点数的正则表达式
        f = codecs.open(Markdown, 'rb', 'utf-8', 'ignore')
        line = f.readline()
        Energy = pattern.findall(line)
        E_fermi.append(float(Energy[0]))
    return E_fermi

def Extract_GSE_Data(data_point,home_directory):
    Efield = []
    Bandgap = []
    for n in data_point:
        EIGENVAL = home_directory + '/'+n+'/EIGENVAL'

        VB, CB = GBE.GetBandEdge(EIGENVAL)

        # print(n,min(CB)-max(VB))
        Efield.append(float(n))
        Bandgap.append(min(CB) - max(VB))

    return Efield,Bandgap

def Extract_GSE_Data_2(data_point,home_directory,E_fermi):
    Efield = []
    Bandgap = []
    for n in data_point:
        EIGENVAL = home_directory + '/' + n + '/EIGENVAL'

        VB, CB = GBE.GetBandEdge_2(EIGENVAL,E_fermi[data_point.index(n)])

        # print(n,min(CB)-max(VB))
        Efield.append(float(n))
        Bandgap.append(min(CB) - max(VB))

    return Efield, Bandgap

def Extract_negative_GSE_Data(data_point,home_directory):
    Efield = []
    Bandgap = []
    for n in data_point:
        EIGENVAL = home_directory + '/'+n+'/EIGENVAL'

        VB, CB = GBE.GetBandEdge(EIGENVAL)

        # print(n,min(CB)-max(VB))
        Efield.append(-float(n.replace('m','')))
        Bandgap.append(min(CB) - max(VB))

    return Efield,Bandgap


def Extract_negative_GSE_Data_2(data_point, home_directory,E_fermi):
    Efield = []
    Bandgap = []
    for n in data_point:
        EIGENVAL = home_directory + '/' + n + '/EIGENVAL'

        VB, CB = GBE.GetBandEdge_2(EIGENVAL,E_fermi[data_point.index(n)])

        # print(n,min(CB)-max(VB))
        Efield.append(-float(n.replace('m', '')))
        Bandgap.append(min(CB) - max(VB))

    return Efield, Bandgap

def reshape(x,y,critical_point):
    x_new = []
    y_new = []
    for i in range(len(x)):
        if x[i] >= critical_point:
            x_new.append(x[i])
            y_new.append(y[i])
        else:
            pass
    return x_new,y_new


def FittedLine(x,Data_x,Data_y):
    slope, intercept, r_value, p_value, std_err = st.linregress(Data_x, Data_y)
    return slope*x+intercept


#a = Extract_Fermi_energy(Data_point_4,home_dir_3_m1)
#print(a)

Ef_2_1 = [-0.2633, -0.2573, -0.2497, -0.2427, -0.2354, -0.228, -0.2204, -0.2129, -0.2053, -0.1977, -0.1901, -0.1921,
          -0.1845, -0.1769, -0.1694, -0.1619, -0.1545, -0.1471, -0.1398, -0.1025, -0.27, -0.2629, -0.2559]
Ef_2_m1 = [-0.2573, -0.2497, -0.2427, -0.2354, -0.228, -0.2204, -0.2129, -0.2053, -0.1977, -0.1901, -0.1921, -0.1845, -0.1769,
           -0.1694, -0.1619, -0.1545, -0.1471, -0.1398, -0.1025, -0.27, -0.2629, -0.2559]
Ef_2_standard = [-0.2633, -0.1441, -0.1396, -0.3009, -0.1676, -0.1908, -0.2996, -0.1689, -0.1525, -0.2098, -0.2917, -0.2907, -0.1488,
                 -0.208, -0.2766, -0.1314, -0.1311, -0.1485, -0.1701, -0.197, -0.2425, -0.2066, -0.2164]

Ef_3_1 = [1.2267, 1.2068, 1.1495, 1.1523, 1.2338, 1.2384, 1.2405, 1.238, 1.2283, 1.2139, 1.3902, 1.3326, 1.3384]
Ef_3_m1 = [1.3384, 1.3326, 1.3902, 1.2139, 1.2283, 1.238, 1.2405, 1.2384, 1.2423, 1.1522, 1.166, 1.2088]

Ef_4_1 = [2.1873, 2.1356, 2.2812, 2.2796, 2.2746, 2.2791, 2.2918, 2.3053, 2.315, 2.2931, 2.3929, 2.3668, 2.3534]
Ef_4_m1 = [2.3534, 2.3668, 2.3929, 2.2928, 2.315, 2.3054, 2.2918, 2.2791, 2.2727, 2.2789, 2.2934, 2.1403]

Ef_5_1 = [2.9397, 3.0049, 2.9711, 2.9248, 3.0387, 2.9971, 3.1065, 3.0607, 3.1647, 3.1099, 3.1108]
Ef_5_m1 = [3.1109, 3.11, 3.1648, 3.0609, 3.1067, 2.9976, 3.0394, 2.9326, 2.9711, 3.0049]



#a,b = Extract_GSE_Data(Data_point_1,home_dir_2,shift_fermi=0.2)
#a,b = Extract_negative_GSE_Data(Data_point_1,home_dir_6,efermi=-0.51,shift_fermi=0.1)
a,b = Extract_GSE_Data(Data_point_0,home_dir_6_1)
#c,d = Extract_GSE_Data(Data_point_5,home_dir_5_1)
#c,d = Extract_negative_GSE_Data(Data_point_6,home_dir_5_m1)
plt.scatter(a,b,color='k')
#plt.scatter(Efield_1,Bandgap_1,color='r',marker='+')
#plt.plot(x0,y0,linestyle='-.',color='k')
plt.title('Giant Stark Effect of bilayer MoS2',fontsize=16)
plt.xlabel('Electric Field (V/A)',fontsize=16)
plt.ylabel('Bandgap (eV)',fontsize=16)
plt.ylim(0,1.3)
plt.xlim(-0.6,0.6)
plt.show()

#print(c)
#print(d)