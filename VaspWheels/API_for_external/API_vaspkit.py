# This script is designed to provide API functions for VASPKIT (https://vaspkit.com/)

import linecache  # Python标准库，内置的函数对于读取数据文件中特定行的内容等任务十分合适
import numpy as np
import pandas as pd

# 一些常用的全局变量
# 此字典存放了常用的轨道组合的信息，可以通过指明键，直接调用所需的原子轨道能带数据
orbitals_dict = {'s': [2], 'p': [3, 4, 5], 'd': [6, 7, 8, 9, 10],
                 'py': [3], 'pz': [4], 'px': [5],
                 'dxy': [6], 'dyz': [7], 'dz2': [8], 'dxz': [9], 'x2-y2': [10],
                 'dx2-y2 pnm idxy': [6, 10],
                 'px pnm ipy': [3, 5]}


# 此函数专用于读取VASPKIT的tag-21生成的能带或者是投影能带数据数据，输出分别为K-path点数，能带数目，能带计算结果
def GetVaspkitBands(data_file):
    info = [linecache.getline(data_file, i + 1) for i in range(2)]  # 读取计算的目标系统的信息
    info_list = [info[i].split() for i in range(len(info))]         # 对信息进行分割并以列表形式储存

    num_kpoints, num_bands = [int(info_list[1][4]), int(info_list[1][5])]  # 从目标系统信息中读取K-path点数以及能带数目

    # 设置要跳过不读取的空白行，方便用pandas统一读取数据文件
    # rows_to_skip = [0,1,2,303,304,605,606,907,908, ..., 14195,14196]  # 用于纠错跟校准
    skiprows = [1+(num_kpoints+2)*i for i in range(num_bands)]+[2+(num_kpoints+2)*i for i in range(num_bands)]
    # print(skiprows)

    # 利用pandas读取能带数据，详情请参考：https://blog.csdn.net/dugushangliang/article/details/117509764
    data = pd.read_csv(data_file, skiprows=skiprows, header=0, sep='\s+', chunksize=num_kpoints)

    data_separated = [chunk for chunk in data]  # 将数据拆分成一段段DataFrame格式的数据组成的列表

    data_array = np.array([data_separated[i].values for i in range(num_bands)])  # 将数据转换为数组形式,方便分析调用

    return num_kpoints,num_bands,data_array

# 此函数可以获取投影K点路径K-path
def GetProjectedKpath(data_file,num_segment=1):
    num_kpoints, num_bands, data_array = GetVaspkitBands(data_file)  # 调用能带提取提取函数，提取能带计算结果
    Kpath = data_array[0][:,0]  # 提取投影到一维的K-path，每一段能带的第零列都是投影K-path
    num_kpoints_segment = int(num_kpoints/num_segment)
    # Python中的range为左闭右开：3 -> [0, 1, 2, 3), 取值为0, 1, 2
    Kpath_nodes = [Kpath[0]]+[Kpath[i*num_kpoints_segment-1] for i in range(1,num_segment+1)]  # K-path上的所有端点的列表，头尾为投影K点路径的起点跟终点
    return Kpath, Kpath_nodes

# 此函数可以获取能带计算结果
def GetBands(data_file,Fermi_adjust=0):
    num_kpoints, num_bands, data_array = GetVaspkitBands(data_file)  # 调用能带提取提取函数，提取能带计算结果

    band_point_coordinate = [[data_array[i, j, 0] for i in range(num_bands) for j in range(num_kpoints)],
                             [data_array[i, j, 1] + Fermi_adjust for i in range(num_bands) for j in range(num_kpoints)]]

    return band_point_coordinate

# 此函数可以获取投影能带的计算结果
def GetProjectedBands(data_file,orbital,Fermi_adjust=0):
    num_kpoints, num_bands, data_array = GetVaspkitBands(data_file)  # 调用能带提取提取函数，提取能带计算结果

    orbital_weight = sum(data_array[:,:,k] for k in orbitals_dict[orbital])  # 计算原子轨道对能带贡献的占比

    # 能带点坐标[[K point], [Energy], [Weight]]
    band_point_coordinate = [[data_array[i,j,0] for i in range(num_bands) for j in range(num_kpoints)],
                             [data_array[i,j,1]+Fermi_adjust for i in range(num_bands) for j in range(num_kpoints)],
                             [orbital_weight[i,j] for i in range(num_bands) for j in range(num_kpoints)]]

    return band_point_coordinate

# 此函数可以在同一副能带图中同时分析两种原子轨道组合
def BiOrbitalAnalysis(data_file,orbital_list,Fermi_adjust=0):
    num_kpoints, num_bands, data_array = GetVaspkitBands(data_file)  # 调用能带提取提取函数，提取能带计算结果

    orbital_weight_list = []
    for i in range(len(orbital_list)):
        orbital_weight = sum(data_array[:, :, k] for k in orbitals_dict[orbital_list[i]])  # 计算原子轨道对能带贡献的占比
        orbital_weight_list.append(orbital_weight)

    orbital_weight_combined = orbital_weight_list[0] - orbital_weight_list[1]

    # 能带点坐标[[K point], [Energy], [Weight]]
    band_point_coordinate = [[data_array[i,j,0] for i in range(num_bands) for j in range(num_kpoints)],
                             [data_array[i,j,1]+Fermi_adjust for i in range(num_bands) for j in range(num_kpoints)],
                             [orbital_weight_combined[i,j] for i in range(num_bands) for j in range(num_kpoints)]]

    return band_point_coordinate
