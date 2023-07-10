# 通用的数据获取函数模块

import pandas as pd

# 此函数可以利用pandas提取文件中的数据，适用于txt、dat、csv等格式的文件
# 数据文件中的数据形式应为两列式，如：第一列为自变量，第二列为因变量
def GetData(data_file, header=None, sep='\s+', **kwargs):
    # 利用pandas提取数据，得到的结果为DataFrame格式
    # header=None，默认没有列名，第一行作为数据读取；数据分隔符sep，默认为'\s+'（指代\f\n\t\r\v这些）
    data_DataFrame = pd.read_csv(data_file, header=header, sep=sep)  # 若设置header=0的话，则第一行为列名，从第二行开始读取
    data_array = data_DataFrame.values  # 将DataFrame格式的数据转换为数组

    rearranging = kwargs['rearranging'] if 'rearranging' in kwargs else False  # 将数据数组重排为列表方便后续分析操作
    index_by = kwargs['index_by'] if 'index_by' in kwargs else 'row'           # 默认按行重排
    nrow, ncol = data_array.shape  # 获取数据数组的维数
    if rearranging:
        data = [data_array[:, i] for i in range(ncol)] if index_by == 'row' else [data_array[i, :] for i in range(nrow)]
    else:
        return data_array

    return data