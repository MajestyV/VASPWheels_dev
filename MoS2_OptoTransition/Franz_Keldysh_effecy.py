# This code is designed for analyzing Franz-Keldysh effect.
import numpy as np
import pandas as pd
import VaspWheels as vw
import matplotlib.pyplot as plt

def Plot_AbsorptionCoefficient():
    plt.rcParams.update({'xtick.direction': 'in', 'ytick.direction': 'in'})  # 设置x轴和y轴刻度线方向向内

    plt.plot(energy, A_0, color='b')
    plt.plot(energy, A_50, color='r')

    plt.xlim(1.6, 2.4)
    plt.ylim(0.02, 0.15)

    plt.show(block=True)

    return

if __name__=='__main__':
    # JCPGH1
    data_file = ('D:/Projects/OptoTransition/Experiment/南科大/临时工作区/Summary_with background.xls')

    data = pd.read_excel(data_file, header=0, sheet_name=None)  # 利用pandas读取excel文件中的数据

    data_DataFrame = data['Data']
    data_array = data_DataFrame.values

    wavelength = data_array[:,0]  # 波长
    background_1 = data_array[:,1]  # 背景底噪 - I
    background_2 = data_array[:, 2]  # 背景底噪 - II
    num_data = data_array.shape[1]-3
    I_reflection = [data_array[:,i] for i in range(3,data_array.shape[1])]  # 各个不同偏压下的反射谱
    Ir_0, Ir_10, Ir_20, Ir_30, Ir_40, Ir_50 = I_reflection
    delta_Ir = [Ir_0-I_reflection[i] for i in range(num_data)]
    modulation_depth = [(Ir_0-I_reflection[i])/Ir_0 for i in range(num_data)]
    md_0, md_10, md_20, md_30, md_40, md_50 = [vw.Experiment.Moving_average(modulation_depth[i],50) for i in range(num_data)]

    Ia_0, Ia_10, Ia_20, Ia_30, Ia_40, Ia_50 = [np.subtract(data_array[:,1],data_array[:, i])
                                         for i in range(3, data_array.shape[1])]  # 各个不同偏压下的差分吸收谱
    absorbance = [np.log10(background_1/I_reflection[i]) for i in range(num_data)]
    A_0, A_10, A_20, A_30, A_40, A_50 = absorbance

    a_0, a_10, a_20, a_30, a_40, a_50 = [2.303*absorbance[i]/(2*100)for i in range(num_data)]  # 各个不同偏压下的吸收系数

    energy = 1240/wavelength

    print(data_array)

    # 画图模块
    Plot_AbsorptionCoefficient()
    #plt.rcParams.update({'xtick.direction': 'in', 'ytick.direction': 'in'})  # 设置x轴和y轴刻度线方向向内

    #plt.plot(wavelength,md_50)

    #plt.show(block=True)

    # 数据保存模块
    #excel_data = np.array([wavelength, md_0, md_10, md_20, md_30, md_40, md_50]).T  # 通过转置（transpose）重整数据
    #vw.WriteExcel(excel_data, saving_directory='C:/Users/13682/OneDrive/Desktop')