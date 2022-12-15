# 此代码囊括了一系列的函数，以实现一系列功能，致力于为第一性原理研究中常见的数据分析与计算提供便利
# 高聚低耦，吾码所宗，以建理论，追本溯源

import codecs
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

class functions:
    """ This class of functions is designed for general data analysis and computation in ab initio study. """
    def __int__(self):
        self.name = functions

    ##############################################################################################################
    # 通用数据提取以及保存模块

    # 此函数可以利用pandas提取txt文件（也适用于dat文件）中的数据
    # txt或dat文件中的数据形式应为两列式，第一列为自变量，第二列为因变量
    def GetData_txt(self,data_file, **kwargs):
        header = kwargs['header'] if 'header' in kwargs else None  # 文件中的数据列，默认为没有列名，第一行作为数据读取
        sep = kwargs['sep'] if 'sep' in kwargs else '\s+'  # 数据分隔符，默认为'\s+'（指代\f\n\t\r\v这些）
        # 利用pandas提取数据，得到的结果为DataFrame格式
        data_DataFrame = pd.read_csv(data_file, header=header, sep=sep)  # 若header=None的话，则设置为没有列名
        data_array = data_DataFrame.values  # 将DataFrame格式的数据转换为数组
        x = data_array[:, 0]  # 默认第一列为自变量
        y = data_array[:, 1]  # 默认第二列为因变量
        return x, y

    # 此函数可以利用pandas提取csv文件中的数据
    def GetData_csv(self, data_file, **kwargs):
        # 一些关于数据文件的参数
        header = kwargs['header'] if 'header' in kwargs else None  # 文件中的数据列，默认为没有列名，第一行作为数据读取
        x_col = kwargs['x_col'] if 'x_col' in kwargs else 0  # 默认第一列为自变量所在列
        y_col = kwargs['y_col'] if 'y_col' in kwargs else 1  # 默认第二列为因变量所在列

        # 利用pandas提取数据，得到的结果为DataFrame格式
        data_DataFrame = pd.read_csv(data_file, header=header)  # 若header=None的话，则设置为没有列名
        data_array = data_DataFrame.values  # 将DataFrame格式的数据转换为数组
        x = data_array[:, x_col]  # 默认第一列为自变量
        y = data_array[:, y_col]  # 默认第二列为因变量

        return x,y

    ##############################################################################################################
    # 可视化分析模块

    # 此函数可以对数据进行三维曲线的可视化
    def Visualize3D_curve(self,x,y,z):
        # 定义图像和三维坐标轴
        fig = plt.figure()
        # ax = plt.axes(projection='3d')  # 也可以使用：ax=Axes3D(fig)
        ax = Axes3D(fig)
        ax.plot3D(x,y,z)
        return

    # 此函数可以对数据进行三维可视化
    def Visualize3D_surface(self, x, y, z):
        # 定义图像和三维坐标轴
        fig = plt.figure()
        # ax = plt.axes(projection='3d')  # 也可以使用：ax=Axes3D(fig)
        ax = Axes3D(fig)
        ax.plot_surface(x, y, z)
        return

    # 此函数可以将三维数据投影成等高线图，适用于多种场景如：势能（能量）面分析，误差最小化等
    def Visualiza_contour(self):
        return

    ##############################################################################################################
    # 常用的运算或是拟合函数


    ##############################################################################################################
    #########################################接下来的部分为特定功能的实现模块###########################################
    ##############################################################################################################
    # V.A.S.P.计算中的结构文件POSCAR的分析模块
    # This function can extract the information of the lattice structure from the POSCAR file.
    def GetStructure(self, POSCAR):
        file = codecs.open(POSCAR, 'rb', 'utf-8', 'ignore')
        line = file.readline()
        lindex = 0
        lattice_vector = []
        atomic_position_raw = []
        while line:
            content = line.split()  # 以空字符（空格，换行'\n'，制表符'\t'等）为分隔符对本行内容做切片 （什么都不填默认为空字符）
            if lindex == 0:
                system = line.split()
            elif lindex == 1:
                scale = float(content[0])
            elif lindex >= 2 and lindex <= 4:
                content = list(map(float, content))
                lattice_vector.append(content)
            elif lindex == 5:
                atom_species = content
            elif lindex == 6:
                num_atom = list(map(float, content))
            elif lindex == 7:
                coordinate = content[0]
            else:
                content = list(map(float, content))
                atomic_position_raw.append(content)

            line = file.readline()
            lindex += 1
        file.close()

        # 重整原子坐标信息，丢弃无意义的部分
        num_total = int(sum(num_atom))  # 将各原子数加起来得到原子总数,记得要替换为整型
        atomic_position = []
        for i in range(num_total):
            atomic_position.append(atomic_position_raw[i])

        structure = {'system': system, 'scale': scale,
                     'atom': atom_species, 'num_atom': num_atom,
                     'coordinate_system': coordinate,
                     'lattice_vector': lattice_vector,
                     'atomic_position': np.array(atomic_position)}  # 将原子坐标信息转换为数组，以防出错
        return structure

    # 这个函数可以通过晶体的三个基矢a, b, c计算晶格常数，但是记得输入必须是个由三个基矢组成的列表：[[a],[b],[c]]，方便解压
    def LatticeParameter(self, lattice_vector):
        # lattice_vector = lattice_vector.tolist()     # 确保输入是个列表，可以解压
        a_vec, b_vec, c_vec = lattice_vector  # 解压a, b, c基矢
        a_vec = np.array(a_vec)  # 将列表转换为数组，防止出错
        b_vec = np.array(b_vec)
        c_vec = np.array(c_vec)
        a = np.linalg.norm(np.array(a_vec), ord=2)  # 向量的二范数即向量的模
        b = np.linalg.norm(np.array(b_vec), ord=2)
        c = np.linalg.norm(np.array(c_vec), ord=2)
        alpha = np.arccos(np.dot(b_vec, c_vec) / (b * c))  # 利用 cos(<a,b>) = a·b/(|a|·|b|)计算向量夹角
        beta = np.arccos(np.dot(a_vec, c_vec) / (a * c))  # 在python中，向量点乘（内积）可以通过np.dot()函数实现
        gamma = np.arccos(np.dot(a_vec, b_vec) / (a * b))
        return a, b, c, alpha, beta, gamma

    # 用于计算不同晶体坐标下的原子间距
    def BondLength(self, Atom_1, Atom_2, lattice_vector):
        a1, a2, a3 = lattice_vector
        lattice = np.mat([a1, a2, a3])
        lattice_T = np.transpose(lattice)
        MetricTensor = np.dot(lattice, lattice_T)  # 应注意，这里要用向量/矩阵的点乘，不是叉乘，不要弄混

        d_vec = np.mat(Atom_1) - np.mat(Atom_2)
        d_sqaure = d_vec * MetricTensor * np.transpose(d_vec)  # 同时，这里也是点乘
        d_sqaure = np.array(d_sqaure)  # 将d_square从矩阵形式转变为数组形式

        return np.sqrt(d_sqaure[0][0])


    ##############################################################################################################
    # 电子和空穴有效质量计算模块


    ##############################################################################################################
    # 弹性模量计算模块（应变-能量分析）

    ##############################################################################################################
    # 未知领域

    # 这个函数可以将GSE计算的有效质量数据写入excel文件
    def ExportEffectiveMassData(self, saving_directory, data, Kpoint, Efield, filename='EffectiveMass'):
        workbook = xlwt.Workbook()

        sheet = workbook.add_sheet('ElectronEffectiveMass', cell_overwrite_ok=True)
        for i in range(len(Efield)):
            sheet.write(i + 1, 0, Efield[i])
            for j in range(len(Kpoint)):
                sheet.write(0, j + 1, Kpoint[j])
                sheet.write(i + 1, j + 1, data[i][j])
        workbook.save(saving_directory + filename + '.xls')
        return

