# This script is designed to provide API functions for VASPKIT (https://vaspkit.com/)

import linecache  # Python标准库，内置的函数对于读取数据文件中特定行的内容等任务十分合适
import numpy as np
import pandas as pd

def GetProjectedBands(data_file):
    info = [linecache.getline(data_file,i+1) for i in range(2)]
    info_list = [info[i].split() for i in range(len(info))]
    print(info_list[0])

    num_kpoints, num_bands = [int(info_list[1][4]),int(info_list[1][5])]

    # rows_to_skip = [0,1,2,303,304,605,606,907,908, ..., 14195,14196]

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

    Orbital = 'd'
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
    #plt.scatter(x_band,y_band,s=2,c=w_band,cmap=cmap,norm=cmap_norm)

    #plt.xlim(Kpath_origin,Kpath_destination)
    #plt.ylim(-5,5)

    #plt.hlines(0, Kpath_origin, Kpath_destination, linewidth=1, linestyles='dashed', colors='w')
    #plt.vlines(1.15113, -5, 5, linewidth=1,linestyles='dashed',colors='w')
    #plt.vlines(1.81573, -5, 5, linewidth=1,linestyles='dashed',colors='w')

    # 生成颜色条
    fig, ax = plt.subplots(figsize=(6, 1))
    fig.subplots_adjust(bottom=0.5)

    fig.colorbar(mpl.cm.ScalarMappable(cmap=cmap,norm=cmap_norm),cax=ax, orientation='horizontal', label='Weight')