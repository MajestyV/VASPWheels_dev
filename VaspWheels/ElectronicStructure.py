# This code is written to extract electronic structure result from V.A.S.P. calculation results.
# 此代码记录了用于分析VASP计算的体系的电子结构的函数

import re, codecs, linecache
import numpy as np

# 一些通用函数

    # 这个函数利用linecache模块，可以从数据文件中读出指定行的信息，并以字符串形式返回
    # 应注意，这个函数的行数从1开始，即line_index=5指要读文件中的第五行
    def GrepLineContent(self,file,line_index):
        return linecache.getline(file,line_index).strip()

########################################################################################################################
# Basic modules (基础模块): Electronic band structure and density of states (DOS) are the two basic features



# 能带提取模块：此函数可以从VASP计算所得的EIGENVAL文件中直接提取能带计算结果
# This function is designed to extract electronic bands data from file EIGENVAL.
def GetEbands(EIGENVAL):
    pattern_int = re.compile(r'-?\d+')  # 匹配整数，用于提取计算参数
    # pattern_float = re.compile(r'-?\d+\.\d+?[Ee]?-?\d+')  # 匹配可能有科学计数法的浮点数的正则表达式, 用于提取数据

    # 提取能带计算时的一些全局参数
    parameter_string = GrepLineContent(EIGENVAL,6)
    parameter = pattern_int.findall(parameter_string)  # 利用正则表达式提取出这一行所有的整数
    num_valence_electrons, num_kpoints, num_bands = parameter
    # 这行第一个数为价电子总数，第二个为k点路径总点数，第三个为能带总数
    num_valence_electrons = int(num_valence_electrons)  # 从文件中读取完的数据形式为字符串，需要转换为整型才能进行后续处理
    num_kpoints = int(num_kpoints)
    num_bands = int(num_bands)

    # 通过循环读取EIGENVAL中的数据
    file = codecs.open(EIGENVAL,'rb','utf-8','ignore')  # Open file, using codecs to uniform coding type
    line = file.readline()
    line_index = 1  # 读取文件时，为了方便，我们设定从一开始，那么line_index=1指文件的第一行
    raw_data = []   # 存放原始数据的列表
    while line:
        if line_index >= 7:  # 为了方便后续的编程跟数据处理，我们从EIGENVAL的第7行开始读
            value = line.split()  # 以空字符（空格，换行'\n'，制表符'\t'等）为分隔符对字符串做切片 （什么都不填默认为空字符）
            value = list(map(float,value))
            raw_data.append(value)

        line = file.readline()
        line_index += 1
    file.close()

    bands = np.zeros((num_bands,num_kpoints))        # 定义一个num_bands行num_kpoints列的矩阵用于存放能带数据
    occupation = np.zeros((num_bands, num_kpoints))  # 同理，定义一个矩阵存放电子占据数据，此矩阵跟能带矩阵具有相同的维度

    # 在EIGENVAL中，数据会按照K点路径顺序排布，每个K点的能带数据可以看作一个循环，那么我们便可以通过不断loop循环来将数据进行分类整理
    nrows_cycle = num_bands+2   # 每个循环的数据行数为：能带数+K点坐标行+空白分割行 = 能带数+2行
    Kpath, Kweight = [[],[]]  # 批量定义空列表准备储存数据，k_path是K点路径，k_weight是K点对应的权重
    for i in range(num_kpoints):
        # 确定各个数据对应的列表引索
        Kindex, band_data_starting = [i*nrows_cycle+1, i*nrows_cycle+2]
        Kpath.append([raw_data[Kindex][0],raw_data[Kindex][1],raw_data[Kindex][2]])  # K点路径
        Kweight.append(raw_data[Kindex][3])
        # 通过循环将能带数据赋值到刚刚创建的矩阵中
        for j in range(num_bands):
            bands[j,i] = raw_data[band_data_starting+j][1]
            occupation[j,i] = raw_data[band_data_starting+j][2]

    data_dict = {'num_kpoints': num_kpoints,          # K点路径上的取点数
                 'num_bands': num_bands,              # 能带数目
                 'Kpath': Kpath,                      # K点路径
                 'Kweight': Kweight,                  # 每个K点对应的权重
                 'bands': np.array(bands),            # 能带数据（最后的输出为二维数组的话，操作空间会更大）
                 'occupation': np.array(occupation)}  # 轨道（能带）占据情况}

    return data_dict