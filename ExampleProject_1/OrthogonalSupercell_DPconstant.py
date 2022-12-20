import numpy as np
import matplotlib.pyplot as plt
from VaspWheels import GetElectronicBands,Visualization

GEB = GetElectronicBands.vasp()
VI = Visualization.plot()

##################################################################################################################
# 提取数据
data_directory = 'D:/Projects/PhaseTransistor/Data/Simulation/CarrierTransport/4/Ort_supercell/Deformation potential constant/DP_constant/'  # 办公室电脑

file_list_x = ['4_x_-0.010','4_x_-0.005','4_x_0.000','4_x_0.005','4_x_0.010']
file_list_y = ['4_y_-0.010','4_y_-0.005','4_y_0.000','4_y_0.005','4_y_0.010']

VBM_x,CBM_x = [[],[]]
for i in file_list_x:
    EIGENVAL = data_directory+i+'/EIGENVAL'
    valence_band, conduction_band = GEB.GetBandEdges(EIGENVAL)
    VBM_x.append(max(valence_band))
    CBM_x.append(min(conduction_band))

VBM_y,CBM_y = [[],[]]
for i in file_list_y:
    EIGENVAL = data_directory+i+'/EIGENVAL'
    valence_band, conduction_band = GEB.GetBandEdges(EIGENVAL)
    VBM_y.append(max(valence_band))
    CBM_y.append(min(conduction_band))

#print(VBM)
#print(CBM)

# 计算Deformation potential constant
strain = np.array([-0.010,-0.005,0.000,0.005,0.010])

coef_x_VBM,coef_x_CBM = [np.polyfit(strain,VBM_x,1),np.polyfit(strain,CBM_x,1)]  # 线性拟合
coef_y_VBM,coef_y_CBM = [np.polyfit(strain,VBM_y,1),np.polyfit(strain,CBM_y,1)]

##################################################################################################################
# 画图模块
VI.GlobalSetting(x_major_tick=0.01,y_major_tick=0.25)

blue = VI.MorandiColor('Paris')
red = VI.MorandiColor('Redred')

# 真实数据
# VI.Visualize(strain,VBM,curve='scatter',marker='s',color=blue,label=r'$\mathbf{a}_{\mathrm{ort},1}$')
# VI.Visualize(strain,CBM,curve='scatter',marker='^',color=red,label=r'$\mathbf{a}_{\mathrm{ort},2}$')
plt.plot(strain, VBM_x, 's', markersize=7, color=blue,label=r'VBM under $\mathbf{a}_{\mathrm{ort},1}$-strain')  # x strain
plt.plot(strain, CBM_x, 's', markerfacecolor='none', markersize=7, color=blue,label=r'CBM under $\mathbf{a}_{\mathrm{ort},1}$-strain')
plt.plot(strain, VBM_y, '^', markersize=7, color=red,label=r'VBM under $\mathbf{a}_{\mathrm{ort},2}$-strain')  # y strain
plt.plot(strain, CBM_y, '^', markerfacecolor='none', markersize=7, color=red,label=r'CBM under $\mathbf{a}_{\mathrm{ort},2}$-strain')

# 拟合结果
strain_mesh = np.linspace(-0.015,0.015,100)
# np.polyval()函数可以通过输入系数跟自变量计算多项式的值
VI.Visualize(strain_mesh,np.polyval(coef_x_VBM,strain_mesh),color=blue,linestyle='dashed')
                                    # label=r'Linear fitting of $\mathbf{a}_{\mathrm{ort},1}$')
VI.Visualize(strain_mesh,np.polyval(coef_x_CBM,strain_mesh),color=blue,linestyle='dashed',)
VI.Visualize(strain_mesh,np.polyval(coef_y_VBM,strain_mesh),color=red,linestyle='dashed')
             # label=r'Linear fitting of $\mathbf{a}_{\mathrm{ort},2}$')
VI.Visualize(strain_mesh,np.polyval(coef_y_CBM,strain_mesh),color=red,linestyle='dashed')

VI.FigureSetting(xlabel='Strain', ylabel='Energy (eV)',xlim=(-0.011,0.011),ylim=(1.5,2.75),
                 legend='True')

saving_directory = 'D:/Projects/PhaseTransistor/Data/Figures/CarrierTransportation/'  # 办公室电脑
VI.SavingFigure(saving_directory,filename='Band edge shifting',format='pdf')