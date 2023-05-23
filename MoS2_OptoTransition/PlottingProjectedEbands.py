import linecache  # Python标准库，内置的函数对于读取数据文件中特定行的内容等任务十分合适
import numpy as np
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib import cm,colors

if __name__=='__main__':
    data_file = 'D:/Projects/OptoTransition/Data/MoS2_ElectronicStructure/Projected_bands/Pentalayer_SYM/Mo/PBAND_SUM.dat'  # MMW502
    # data_file = 'D:/Projects/OptoTransition/Data/MoS2_ElectronicStructure/Projected_bands/PBANDS_SOC/Mo/PBAND_SUM_SOC.dat'  # JCPGH1

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

    #x_band, y_band, weight_band = [[],[],[]]  # 用于存放能带图上，每一个散点的坐标
    #for i in range(num_bands):
        #for j in range(num_kpoints):
            # x_coordinate = (data_array[i,j,0],data_array[i,j,1])
            #x_band.append(data_array[i,j,0])
            #y_band.append(data_array[i,j,1])
            #weight_band.append(data_array[i,j,11])

    Orbital = 'dz2'
    Orbitals_index ={'s':[2], 'p': [3,4,5], 'd': [6,7,8,9,10],
                     'py':[3], 'pz':[4], 'px':[5],
                     'dxy':[6], 'dyz':[7], 'dz2':[8], 'dxz':[9], 'x2-y2':[10]}
    Orbital_weight = sum(data_array[:,:,k] for k in Orbitals_index[Orbital])  # 计算原子轨道对能带贡献的占比

    # w_band = [Orbital_weight[i,j] for i in range(num_bands) for j in range(num_kpoints)]

    Fermi_factor = 0.2863  # 费米面调零参数

    Band_point_coordinate = [[data_array[i,j,0] for i in range(num_bands) for j in range(num_kpoints)],
                             [data_array[i,j,1]+Fermi_factor for i in range(num_bands) for j in range(num_kpoints)],
                             [Orbital_weight[i,j] for i in range(num_bands) for j in range(num_kpoints)]]

    x_band,y_band,w_band = Band_point_coordinate

    # 画图模块
    plt.rcParams['axes.facecolor'] = np.array([0,0,128])/255.0  # 更换背景颜色

    cmap = 'jet'
    cmap_norm = colors.Normalize(0,1)

    # 画投影能带
    # https://blog.shishiruqi.com//2019/05/19/pymatgen-band/
    # 用Matplotlib绘制渐变的彩色曲线：https://blog.csdn.net/xufive/article/details/127492212
    # 利用散点图实现渐变：https://www.brothereye.cn/python/427/
    plt.scatter(x_band,y_band,s=2,c=w_band,cmap=cmap,norm=cmap_norm)

    plt.xlim(Kpath_origin,Kpath_destination)
    plt.ylim(-5,5)

    plt.hlines(0, Kpath_origin, Kpath_destination, linewidth=1, linestyles='dashed', colors='w')
    plt.vlines(1.15113, -5, 5, linewidth=1,linestyles='dashed',colors='w')
    plt.vlines(1.81573, -5, 5, linewidth=1,linestyles='dashed',colors='w')

    # 生成颜色条
    #fig, ax = plt.subplots(figsize=(6, 1))
    #fig.subplots_adjust(bottom=0.5)

    #fig.colorbar(mpl.cm.ScalarMappable(cmap=cmap,norm=cmap_norm),cax=ax, orientation='horizontal', label='Weight')




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