import linecache  # Python标准库，内置的函数对于读取数据文件中特定行的内容等任务十分合适
import numpy as np
import pandas as pd

if __name__=='__main__':
    data_file = 'D:/Projects/OptoTransition/Data/MoS2_ElectronicStructure/Monolayer/Fatbands/PBAND_SUM.dat'

    info = [linecache.getline(data_file,i+1) for i in range(2)]
    info_list = [info[i].split() for i in range(len(info))]
    print(info_list[1])

    num_kpoints, num_bands = [float(info_list[1][4]),float(info_list[1][5])]

    data = pd.read_csv(data_file,header=2,chunksize=num_kpoints+1)

    data_seperated = [chunk for chunk in data]
    print(data_seperated[47])

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
