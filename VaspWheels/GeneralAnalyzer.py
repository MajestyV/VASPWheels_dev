# 此代码囊括了一系列的函数，以实现一系列功能，致力于为第一性原理研究中常见的数据分析与计算提供便利
# 高聚低耦，吾码所宗，以建理论，追本溯源

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

class functions:
    """ This class of functions is designed for general data analysis and computation in ab initio study. """
    def __int__(self):
        self.name = functions

    ##############################################################################################################
    # 数据提取模块

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
    # 计算模块

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
    # 数据保存模块

    # 这个函数可以将GSE计算的有效质量数据写入excel文件
    def ExportEffectiveMassData(self,saving_directory, data, Kpoint, Efield, filename='EffectiveMass'):
        workbook = xlwt.Workbook()

        sheet = workbook.add_sheet('ElectronEffectiveMass', cell_overwrite_ok=True)
        for i in range(len(Efield)):
            sheet.write(i + 1, 0, Efield[i])
            for j in range(len(Kpoint)):
                sheet.write(0, j + 1, Kpoint[j])
                sheet.write(i + 1, j + 1, data[i][j])
        workbook.save(saving_directory + filename + '.xls')
        return

