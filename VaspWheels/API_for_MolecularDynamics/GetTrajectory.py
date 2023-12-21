# This module is designed for extracting data from classical molecular dynamics simulation.
# LAMMPS:
# https://www.lammps.org/#gsc.tab=0
# https://www.lammps.org.cn/ (中文网站)

import linecache
import numpy as np
import pandas as pd

def GetTraj_LAMMPS(data_file):
    system_info = [[linecache.getline(data_file, i + 1)] for i in range(9)]  # 读取目标系统的信息，应注意lincache函数默认从1开始

    num_atom = int(system_info[3][0])  # 读取目标系统的原子个数，即为系统信息的第四行

    nline_per_timestep = num_atom + 9  # 每一个分块的行数

    with open(data_file) as file:
        for num_line, _ in enumerate(file, 1):
            pass

    num_timestep = int(num_line / nline_per_timestep)  # 总共的采样步数
    timestep = np.array(
        [float(linecache.getline(data_file, 2 + i * nline_per_timestep)) for i in range(num_timestep)])  # 时间步
    print(timestep)

    rows_to_skip = []  # 跳过一些冗余的信息行
    for i in range(num_timestep):
        for j in [0, 1, 2, 3, 4, 5, 6, 7, 8]:
            rows_to_skip.append(i * nline_per_timestep + j)

    # 利用pandas读取molecular dynamic轨迹
    data_chunks = pd.read_csv(data_file, header=None, skiprows=rows_to_skip, sep='\s+', chunksize=num_atom)  # 分块读取
    # 数据整理及转化
    data_DataFrame = [chunk for chunk in data_chunks]  # DataFrame格式的数据
    data_list = [data_DataFrame[i].values for i in range(num_timestep)]

    return system_info, timestep, data_list

if __name__=='__main__':
    data_file = 'D:/Projects/PINN/Data/Si_melting_example/traj_nvt.lammpstrj'

    system_info, timestep, data_list = GetTraj_LAMMPS(data_file)



    # data_list = []
    # for chunk in data_chunks:
        # print(chunk)

    # print(data_chunks.get_chunk(0))