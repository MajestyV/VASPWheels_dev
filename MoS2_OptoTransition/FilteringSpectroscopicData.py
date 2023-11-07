import numpy as np
import pandas as pd
import VaspWheels as vw
import matplotlib.pyplot as plt
from matplotlib import cm

def Get_excel(data_file, sheet_list):
    # 设置sheet_name=None，可以读取全部的sheet，返回字典，key为sheet名字，value为sheet表内容
    data = pd.read_excel(data_file, sheet_name=None)  # 利用pandas读取excel文件中的数据

    example_sheet = 'Data'  # 每一个老4200的数据文件都一定有Data这一页数据，可以利用这一页来取得4200中测试的项目
    # .columns.values.tolist()，这个命令可以得到数据表格的表头，也就是4200中测试的项目，如：Time, AI, BI ......
    title = data[example_sheet].columns.values.tolist()  # 数据的表头将以列表的形式储存
    num_charac = len(title)  # 测试的性能的个数（number of characteristics）
    num_cycle = len(sheet_list)  # 测试循环的次数即数据表格的个数

    extracted_data = [[] for i in range(num_cycle)]  # 按照测试循环的个数，将文件中的数据提取并分类到此表格中
    for i in sheet_list:
        sheet_index = sheet_list.index(i)  # 寻找字符串i在列表sheet_list中的索引，用于后续数据的分类
        sheet_data = data[i].values  # 将名字为变量i所指的字符串的那页（以下称sheet_i）提取出来的DataFrame数据转换成列表
        for j in range(num_charac):
            extracted_data[sheet_index].append(sheet_data[:, j])
            # 将sheet_i的数据按照项目名称重新整理到名为extracted_data的列表中
            # [[sheet1的数据], [sheet2的数据], [sheet3的数据], ...]
            # 而其中，[sheetX的数据] = [[测试项目1的数据], [测试项目2的数据], [测试项目3的数据], ...]

    return title, extracted_data

def DifferentialAbsorption():
    data_file = ('E:/Projects/OptoTransition/Experiment/南科大/临时工作区/DifferentialAbsorption.xls')

    data = pd.read_excel(data_file, sheet_name=None)  # 利用pandas读取excel文件中的数据

    data_DataFrame = data['Sheet1']
    data_array = data_DataFrame.values

    windowsize = 10
    wavelength = data_array[:, 0]
    E_photon = data_array[:, 1]
    data_filtered_10V = vw.Experiment.Moving_average(data_array[:, 2], windowsize)
    data_filtered_20V = vw.Experiment.Moving_average(data_array[:, 3], windowsize)
    data_filtered_50V = vw.Experiment.Moving_average(data_array[:, 6], windowsize)

    plt.plot(wavelength, data_filtered_10V)
    plt.plot(wavelength, data_filtered_20V)
    plt.plot(wavelength, data_filtered_50V)

    return

if __name__=='__main__':
    # JCPGH1
    data_file = ('D:/Projects/OptoTransition/Experiment/南科大/临时工作区/Absorption.xls')

    data = pd.read_excel(data_file, sheet_name=None)  # 利用pandas读取excel文件中的数据

    data_DataFrame = data['Sheet1']
    data_array = data_DataFrame.values

    for i in range(len(data_array)):
        for j in range(len(data_array[0])):
            if j >= 2:
                data_array[i,j] = float(data_array[i,j])
            else:
                pass

    windowsize = 50
    wavelength = data_array[:,0]
    E_photon = data_array[:,1]
    data_filtered_0V = vw.Experiment.Moving_average(data_array[:,2], windowsize)
    data_filtered_10V = vw.Experiment.Moving_average(data_array[:, 3], windowsize)
    data_filtered_20V = vw.Experiment.Moving_average(data_array[:, 4], windowsize)
    data_filtered_30V = vw.Experiment.Moving_average(data_array[:, 5], windowsize)
    data_filtered_40V = vw.Experiment.Moving_average(data_array[:, 6], windowsize)
    data_filtered_50V = vw.Experiment.Moving_average(data_array[:, 7], windowsize)

    dA_10V = data_filtered_0V-data_filtered_10V
    dA_20V = data_filtered_0V-data_filtered_20V
    dA_30V = data_filtered_0V-data_filtered_30V
    dA_40V = data_filtered_0V-data_filtered_40V
    dA_50V = data_filtered_0V-data_filtered_50V

    # 画图模块
    plt.rcParams.update({'xtick.direction': 'in', 'ytick.direction': 'in'})  # 设置x轴和y轴刻度线方向向内

    #plt.plot(wavelength, data_filtered_0V)
    #plt.plot(wavelength,data_filtered_10V)
    #plt.plot(wavelength,data_filtered_20V)
    #plt.plot(wavelength, data_filtered_30V)
    #plt.plot(wavelength, data_filtered_40V)
    #plt.plot(wavelength,data_filtered_50V)
    #plt.xlim(500,750)

    # 获取colormap: matplotlib.cm.get_cmap(name=None, lut=None)
    # name：内置 colormap 的名称，如 'viridis'(默认)，'spring' 等
    # lut：整数，重置 colormap 的采样间隔，默认是256
    n = 9
    hot = cm.get_cmap('afmhot', n)
    hot_list = [[hot(i)[0],hot(i)[1],hot(i)[2]] for i in range(n)]

    print(hot_list)

    #plt.plot(E_photon, dA_10V, c=hot_list[5])
    #plt.plot(E_photon, dA_20V, c=hot_list[4])
    #plt.plot(E_photon, dA_30V, c=hot_list[3])
    #plt.plot(E_photon, dA_40V, c=hot_list[2])
    #plt.plot(E_photon, dA_50V, c=hot_list[1])
    #plt.xlim(1.6, 3.0)
    #plt.ylim(-50, 900)
    plt.plot(wavelength, dA_10V, c=hot_list[5])
    plt.plot(wavelength, dA_20V, c=hot_list[4])
    plt.plot(wavelength, dA_30V, c=hot_list[3])
    plt.plot(wavelength, dA_40V, c=hot_list[2])
    plt.plot(wavelength, dA_50V, c=hot_list[1])
    plt.xlim(550, 750)
    plt.ylim(-50, 900)

    excel_data = np.array([wavelength,dA_10V,dA_20V,dA_30V,dA_40V,dA_50V]).T  # 通过转置（transpose）重整数据
    vw.WriteExcel(excel_data,saving_directory='D:/Projects/OptoTransition/Experiment/南科大/临时工作区')



    # print(data_array)
