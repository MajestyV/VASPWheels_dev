import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from os import path

default_path = path.join(path.expanduser("~"), 'Desktop')  # 设置桌面文件夹为默认读写目录

########################################################################################################################
# 数据保存模块

# 此函数通过numpy的savetxt函数保存数据
def SavingData(data, sep=' ', saving_directory=default_path, file_name='untitled'):
    saving_address = saving_directory + '/' + file_name + '.txt'  # 储存地址
    np.savetxt(saving_address, data, delimiter=sep)
    return

# 此函数利用pandas包记录数据，并储存为CSV形式的文件，方便excel读取并分析处理，应注意输入的数据应为二维数组或是二维列表
def WriteCSV(data, sep = ' ', saving_directory=default_path, file_name='untitled', format='csv', **kwargs):
    saving_address = saving_directory + '/' + file_name + '.txt'  # 储存地址

    data = np.array(data)  # 确保输入数据为二维数组
    shape = data.shape  # 获取data的维数
    row_index = kwargs['row_index'] if 'row_index' in kwargs else [i + 1 for i in range(shape[0])]  # 行引索
    col_index = kwargs['col_index'] if 'col_index' in kwargs else [i + 1 for i in range(shape[1])]  # 列引索
    data_df = pd.DataFrame(data, index=row_index, columns=col_index)  # 将数据转换为pandas专用的DataFrame格式

    data_df.to_csv(saving_address, index=True, header=True, sep=sep)  # 保存数据

    # 在csv文件中第一行添加分隔符信息，这样子excel读取csv文件的时候才不会排版错乱
    with open(saving_address, 'r+', encoding='utf-8') as file:
        content = file.read()                      # 将已有的内容读取出来
        file.seek(0, 0)                            # 找到数据文件的开头
        file.write('sep=' + sep + '\n' + content)  # 写入分隔符信息
    return

########################################################################################################################
# 图像保存模块

# 此函数专用于保存利用matplotlib包绘制的图像
def SavingFigure(format='jpg', dpi=600, saving_directory=default_path, file_name='untitled'):
    saving_address = saving_directory + '/' + file_name + '.' + format  # 储存地址
    plt.savefig(saving_address, dpi=dpi, format=format)
    return