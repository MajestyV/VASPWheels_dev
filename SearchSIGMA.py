import re
import codecs
import numpy as np
import scipy.stats as st
import matplotlib.pyplot as plt
from VaspWheels import AnalyzeBandgap
from VaspWheels import GetKpath

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
# home_dir_4 = 'H:/Raw_Data/GSE_pawpbe_SOC_MoS2/2_D3BJ_GSE_1'
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


EIGENVAL = home_dir_4_1+'/0.000/EIGENVAL'
# K_path = home_dir_4_1+'/0.000/K-path'

def ExtractKPOINTS(KPOINTS):
    f = codecs.open(KPOINTS, 'rb', 'utf-8', 'ignore')
    l = f.readline()
    lindex = 0
    data = []
    while l:
        if lindex >= 3:
            value = l.split()
            value = list(map(float,value))
            data.append(value)
        l = f.readline()
        lindex += 1
    f.close()
    return data


vb,cb = GBE.GetBandEdge(EIGENVAL)
#print(vb,cb)

search_range=[]
for i in range(len(cb)):
    if i >= 225:
        search_range.append(cb[i])
E_sigma = min(search_range)
index = cb.index(E_sigma)

# K = ExtractKPOINTS(K_path)

for n in Data_point_3:
    K_path = home_dir_4_1+'/'+n+'/K-path'
    K = ExtractKPOINTS(K_path)
    print(K[index])

#print(K)
#print(index)
#print(K[index])



#print(max(vb),min(cb))
#print(min(cb)-max(vb))

#x = range(len(vb))
#plt.plot(x,vb)
#plt.plot(x,cb)
