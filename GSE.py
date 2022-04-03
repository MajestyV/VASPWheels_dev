import re
import codecs
import numpy as np
import scipy.stats as st
import matplotlib.pyplot as plt
from VaspWheels import GetBandEdge

GBE = GetBandEdge.BandEdge()

home_dir = 'D:/Data/MoS2/GSE/pawpbe_vasp5_SOC/2/2_D2ISIF4_GSE/Iterative_SettingTest2'
home_dir_1 = 'D:/Data/MoS2/GSE/pawpbe_vasp5_SOC/2/2_D2ISIF4_GSE/Iterative_SettingTest3'
home_dir_2 = 'D:/Data/MoS2/GSE/pawpbe_vasp5_SOC/2/2_D3BJ_GSE/2_D3BJ_GSE_Iterative'
home_dir_3 = 'D:/Data/MoS2/GSE/pawpbe_vasp5_SOC/2/2_D3BJ_GSE/2_D3BJ_GSE_m1'
home_dir_4 = 'D:/Data/MoS2/GSE/pawpbe_vasp5_SOC/3/3_D3BJ_GSE_1'
home_dir_5 = 'D:/Data/MoS2/GSE/pawpbe_vasp5_SOC/3/3_D3BJ_GSE_m1'
home_dir_6 = 'D:/Data/MoS2/GSE/pawpbe_vasp5/2_D3BJ_GSE_1'
# home_dir_4 = 'H:/Raw_Data/GSE_pawpbe_SOC_MoS2/2_D3BJ_GSE_1'
Data_point_1 = ['0.025','0.050','0.075','0.100','0.125','0.150','0.175','0.200','0.225','0.250','0.275','0.300',
                '0.325','0.350','0.375','0.400','0.425','0.450','0.475','0.500','0.550']
Data_point_2 = ['0.000','0.010','0.020','0.030','0.040','0.050','0.060','0.070','0.080','0.090',
                '0.100','0.110','0.120','0.130','0.140','0.150','0.160','0.170','0.180','0.190',
                '0.200','0.210','0.220','0.230','0.240','0.250','0.260','0.270','0.280','0.290',
                '0.300','0.310','0.320','0.330','0.340','0.350','0.360','0.370','0.380','0.390',
                '0.400','0.410','0.420','0.430','0.440','0.450','0.460','0.470','0.480','0.490',
                '0.500']
# 0.320
Data_point_3 = ['m0.025','m0.075','m0.100','m0.125','m0.150','m0.175','m0.200','m0.225','m0.250','m0.275','m0.300',
                'm0.325','m0.350']

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

def Extract_GSE_Data(data_point,home_directory,efermi="",ground_state='0.025',shift_fermi=0):
    if not efermi:
        baseline = home_directory+'/'+ground_state+'/Markdown_SCF'  # file that contains the ground state Fermi energy (baseline)
        efermi = GBE.GetEfermi(baseline,shift_fermi)
    else:
        efermi = efermi+shift_fermi

    Efield = []
    Bandgap = []
    for n in data_point:
        EIGENVAL = home_directory + '/'+n+'/EIGENVAL'

        VB, CB = GBE.GetBandEdge(EIGENVAL, efermi)

        # print(n,min(CB)-max(VB))
        Efield.append(float(n))
        Bandgap.append(min(CB) - max(VB))

    return Efield,Bandgap

def Extract_negative_GSE_Data(data_point,home_directory,efermi="",ground_state='0.000',shift_fermi=0):
    if not efermi:
        baseline = home_directory+'/'+ground_state+'/Markdown_SCF'  # file that contains the ground state Fermi energy (baseline)
        efermi = GBE.GetEfermi(baseline,shift_fermi)
    else:
        efermi = efermi+shift_fermi

    Efield = []
    Bandgap = []
    for n in data_point:
        EIGENVAL = home_directory + '/'+n+'/EIGENVAL'

        VB, CB = GBE.GetBandEdge(EIGENVAL, efermi)

        # print(n,min(CB)-max(VB))
        Efield.append(-float(n.replace('m','')))
        Bandgap.append(min(CB) - max(VB))

    return Efield,Bandgap

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


# print(Check_GSE_Data(Data_point_1,home_dir_3))
#Efield_reshape,Bandgap_reshape = reshape(Efield,Bandgap,0.1)
#x0 = np.linspace(0,0.6,1000)
#y0 = FittedLine(x0,Efield_reshape,Bandgap_reshape)
#print(Efield)
#print(Bandgap)
#print(y0)
#a,b = Extract_GSE_Data(Data_point_1,home_dir_2,shift_fermi=0.2)
#a,b = Extract_negative_GSE_Data(Data_point_1,home_dir_6,efermi=-0.51,shift_fermi=0.1)
c,d = Extract_GSE_Data(Data_point_1,home_dir_6,shift_fermi=0.1)
plt.scatter(c,d,color='k')
#plt.scatter(Efield_1,Bandgap_1,color='r',marker='+')
#plt.plot(x0,y0,linestyle='-.',color='k')
plt.title('Giant Stark Effect of bilayer MoS2',fontsize=16)
plt.xlabel('Electric Field (V/A)',fontsize=16)
plt.ylabel('Bandgap (eV)',fontsize=16)
plt.ylim(0,1.3)
plt.xlim(-0.6,0.6)
plt.show()

