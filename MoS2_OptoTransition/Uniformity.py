import numpy as np
import matplotlib.pyplot as plt


import pandas as pd

# 此函数可以利用pandas提取文件中的数据，适用于txt、dat、csv等格式的文件
# 数据文件中的数据形式应为两列式，如：第一列为自变量，第二列为因变量
def GetData(data_file, header=None, sep='\s+', **kwargs):
    # 利用pandas提取数据，得到的结果为DataFrame格式
    # header=None，默认没有列名，第一行作为数据读取；数据分隔符sep，默认为'\s+'（指代\f\n\t\r\v这些）
    data_DataFrame = pd.read_csv(data_file, header=header, sep=sep)  # 若设置header=0的话，则第一行为列名，从第二行开始读取
    data_array = data_DataFrame.values  # 将DataFrame格式的数据转换为数组

    rearranging = kwargs['rearranging'] if 'rearranging' in kwargs else False  # 将数据数组重排为列表方便后续分析操作
    index_by = kwargs['index_by'] if 'index_by' in kwargs else 'row'           # 默认按行重排
    nrow, ncol = data_array.shape  # 获取数据数组的维数
    if rearranging:
        data = [data_array[:, i] for i in range(ncol)] if index_by == 'row' else [data_array[i, :] for i in range(nrow)]
    else:
        return data_array

    return data


if __name__=='__main__':
    x, y = (21,21)
    excitation_wavelength = 529.8  # [=] nm
    baseline = 800  # 基线强度

    data_file = '/Users/liusongwei/OptoTransition/Experiment/南科大/Uniformity.csv'

    data_DataFrame = pd.read_csv(data_file, header=None, sep=',')
    data_array = data_DataFrame.values

    data_length, num_data = data_array.shape  # 从数据的形状中获取出数据长度以及数据点个数

    wavelength = data_array[:, 0]  # 第一列数据为测试波长

    excitation_photon_energy = 1239.8/excitation_wavelength
    print(excitation_photon_energy)

    photon_energy = 1239.8/wavelength
    energy_shift = photon_energy-excitation_photon_energy
    wavenumber_shift = 8065.5*energy_shift
    print(wavenumber_shift)

    data = np.empty((x,y,data_length))  # 创建空数据以存放数据
    for n in range(x):
        for m in range(y):
            data[n,m] = data_array[:,n*m+1]-baseline  # 第一列数据为测试波长


    plt.plot(wavenumber_shift,data[0,0])

    # print(data)



    #for i in range():
    #print(data_DataFrame)
