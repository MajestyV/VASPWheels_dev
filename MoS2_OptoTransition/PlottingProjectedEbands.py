import linecache  # Python标准库，内置的函数对于读取数据文件中特定行的内容等任务十分合适
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

if __name__=='__main__':
    # data_file = 'D:/Projects/OptoTransition/Data/MoS2_ElectronicStructure/Monolayer/Mo1/PBAND_SUM.dat'  # MMW502
    data_file = 'D:/Projects/OptoTransition/Data/MoS2_ElectronicStructure/Monolayer/Mo1/PBAND_SUM.dat'  # JCPGH1

    info = [linecache.getline(data_file,i+1) for i in range(2)]
    info_list = [info[i].split() for i in range(len(info))]
    print(info_list[0])

    num_kpoints, num_bands = [int(info_list[1][4]),int(info_list[1][5])]

    rows_to_skip = [0,1,2,303,304,605,606,907,908, ..., 14195,14196]

    skiprows = [1+(num_kpoints+2)*i for i in range(num_bands)]+[2+(num_kpoints+2)*i for i in range(num_bands)]

    # print(skiprows)

    data = pd.read_csv(data_file,skiprows=skiprows,header=0,sep='\s+',chunksize=num_kpoints)
    # https://blog.csdn.net/dugushangliang/article/details/117509764

    data_separated = [chunk for chunk in data]  # 将数据拆分成一段段DataFrame格式的数据组成的列表
    # print(data_separated[44])

    data_array = np.array([data_separated[i].values for i in range(num_bands)])  # 将数据转换为数组形式,方便分析调用
    print(data_array[44])

    Kpath_origin, Kpath_destination = [min(data_array[0][:,0]),max(data_array[0][:,0])]  # 获取投影K点路径的起点跟终点

    Band_points_x, Band_points_y,Band_points_weight = [[],[],[]]  # 用于存放能带图上，每一个散点的坐标
    for i in range(num_bands):
        for j in range(num_kpoints):
            # x_coordinate = (data_array[i,j,0],data_array[i,j,1])
            Band_points_x.append(data_array[i,j,0])
            Band_points_y.append(data_array[i,j,1])
            Band_points_weight.append(data_array[i,j,11])

    plt.scatter(Band_points_x,Band_points_y,c=Band_points_weight,cmap='viridis')


    #for i in range(num_bands):
        #Kpath_projected = data_array[i][:,0]
        #Energy = data_array[i][:,1]

        #plt.plot(Kpath_projected,Energy)

    plt.xlim(Kpath_origin,Kpath_destination)
    plt.ylim(-5,5)

    plt.vlines(1.15113, -5, 5)
    plt.vlines(1.81573, -5, 5)





    # (data_separated[46]['s'])

    #data_separated = []
    #for chunk in data:
        #chunk_filtered = chunk[chunk['# Band-Index    1'].str.contains('Band-Index') == False]
        #data_separated.append(chunk_filtered)

    #print(data_separated[46])

    # 如何在Pandas中删除包含特定值的行
    # https://geek-docs.com/pandas/pandas-examples/how-to-drop-rows-that-contain-a-specific-value-in-pandas.html



    #param_line_1 = linecache.getline(data_file,1)  # 应注意，getline函数中的行数变量是文件中的真实函数，如：1代表了文件中的第一行
    #param_list_1 = (param_line_1.split('\s+'))
    #param_line_2 = linecache.getline(data_file,2)
    #print(content)
    #print(content.split())

    #data = pd.read_csv(data_file,header=2,chunksize=301)

    #a = []
    #for chunk in data:
        #a.append(chunk)
        # print(chunk)

    #print(a[47])

    # print(data[1])

    # 画投影能带
    # https://blog.shishiruqi.com//2019/05/19/pymatgen-band/
    # 用Matplotlib绘制渐变的彩色曲线：https://blog.csdn.net/xufive/article/details/127492212
    # 利用散点图实现渐变：https://www.brothereye.cn/python/427/
