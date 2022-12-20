import numpy as np
import matplotlib.pyplot as plt
from VaspWheels import GeneralAnalyzer,Visualization

GA = GeneralAnalyzer.functions()  # 调用GeneralAnalyzer模块
VI = Visualization.plot()         # 调用Visualization模块

###################################################################################################################
# 数据提取及处理
data_directory = 'D:/Projects/PhaseTransistor/Data/Simulation/CarrierTransport/4/Ort_supercell/Manual optimization/strain-energy profile/'  # 办公室电脑

filename = ['4_LocalMinimum_x_strain.dat','4_LocalMinimum_y_strain.dat']

# 提取数据
x_strain,x_energy = GA.GetData(data_directory+filename[0],header=0)  # 设置header=0，则第一行会作为列名读取
y_strain,y_energy = GA.GetData(data_directory+filename[1],header=0)

# 数据调零函数
def ShiftOrigin(array): return array-min(array)

x_energy, y_energy = [ShiftOrigin(x_energy), ShiftOrigin(y_energy)]

x_coef = np.polyfit(x_strain,x_energy,2)  # 对于简单的二次项回归np.polyfit()函数会更加robust
y_coef = np.polyfit(y_strain,y_energy,2)  # 系数的排列从高到低，比如对于二次多项式，系数对于的次数依次为：2、1、0

print(y_coef)

Area = 3.177889527334834*5.50431706707831

print(GA.ElasticModulus(x_strain,x_energy,Area))
print(GA.ElasticModulus(y_strain,y_energy,Area))

#print(parameter1,parameter2)
#print(-coef1[1]/(2*coef1[0]))
#print(-coef2[1]/(2*coef2[0]))
#print((0.01685448119947595+0.01952792991364153)/2)

###################################################################################################################
# 画图模块
VI.GlobalSetting(x_major_tick=0.05,y_major_tick=0.5)

blue = VI.MorandiColor('Paris')
red = VI.MorandiColor('Redred')

# 真实数据
VI.Visualize(x_strain,x_energy,curve='scatter',marker='s',color=blue,label=r'$\mathbf{a}_{\mathrm{ort},1}$')
VI.Visualize(y_strain,y_energy,curve='scatter',marker='^',color=red,label=r'$\mathbf{a}_{\mathrm{ort},2}$')

# 拟合结果
strain = np.linspace(-0.07,0.07,100)
# np.polyval()函数可以通过输入系数跟自变量计算多项式的值
VI.Visualize(strain,np.polyval(x_coef,strain),color=blue,label=r'Polynomial fitting of $\mathbf{a}_{\mathrm{ort},1}$')
VI.Visualize(strain,np.polyval(y_coef,strain),color=red,label=r'Polynomial fitting of $\mathbf{a}_{\mathrm{ort},2}$')

VI.FigureSetting(xlabel='Strain', ylabel='Energy (eV)',
                 xlim=(-0.065,0.065),ylim=(-0.1,1.75),
                 legend='True')

saving_directory = 'D:/Projects/PhaseTransistor/Data/Figures/CarrierTransportation/'  # 办公室电脑
VI.SavingFigure(saving_directory,filename='Strain-energy profile',format='pdf')