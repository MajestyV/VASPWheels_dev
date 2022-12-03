# 此代码囊括了一系列的函数，以实现一系列功能，致力于为第一性原理研究中常见的数据分析与计算提供便利
# 高聚低耦，吾码所宗，以建理论，追本溯源

import numpy as np
import pandas as pd

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