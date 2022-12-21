from VaspWheels import GetElectronicBands,Visualization

GEB = GetElectronicBands.vasp()  #
VI = Visualization.plot()  #

aList = [1,2,3,4]
aList.reverse()
print(aList)

def Untitled(band_edge):
    band_extracted_1 = list(band_edge[200:300])
    band_extracted_1.reverse()  # 将此段能带翻转
    band_extracted_2 = band_edge[270:299]
    band_extracted_3 = band_edge[201:220]
    return band_extracted_2+band_extracted_1+band_extracted_3

data_directory = 'D:/PhD_research/Data/Simulation/MoS2/GSE/4/4_D3BJ_GSE_1_more_bands/'  # 宿舍电脑

Efield = ['0.000','0.025','0.050','0.075','0.100','0.125','0.150',
          '0.175','0.200']

x = range(0,148,1)

for i in range(len(Efield)):
    EIGENVAL = data_directory+'/'+Efield[i]+'/EIGENVAL'
    valence_band, conduction_band = GEB.GetBandEdges(EIGENVAL)  # 提取导带跟价带
    a = Untitled(valence_band)
    b = Untitled(conduction_band)
    # x = range(0,len(a),1)
    # print(len(a),len(b))
    VI.Visualize(x,a)
    VI.Visualize(x,b)
