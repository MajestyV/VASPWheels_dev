import xlwt
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

    print("csv格式表格写入数据成功！")

    return

# 此函数可以将二维数组形式的数据写入Excel文件
def WriteExcel(data, saving_directory=default_path, file_name='untitled', **kwargs):
    data = np.array(data)  # 数据转换，确保data的形式为numpy二维数组，防止出bug
    num_row, num_col = data.shape  # 获取数据的维度，（行数，列数）

    sheet_name = kwargs['sheet_name'] if 'sheet_name' in kwargs else 'data'  # 默认的表格名称
    write_title = kwargs['write_title'] if 'write_title' in kwargs else True  # 默认写入数据标题
    title = kwargs['title'] if 'title' in kwargs else ['col_'+str(i) for i in range(num_col)]  # 默认的数据标题

    workbook = xlwt.Workbook()  # 新建一个工作簿
    sheet = workbook.add_sheet(sheet_name)  # 在工作簿中新建一个表格

    if write_title:
        for i in range(num_col):
            sheet.write(0, i, title[i])  # 写入标题
        for i in range(num_row):
            for j in range(num_col):
                sheet.write(i+1, j, data[i][j])  # 像表格中写入数据（对应的行和列）
    else:
        for i in range(num_row):
            for j in range(num_col):
                sheet.write(i, j, data[i][j])  # 像表格中写入数据（对应的行和列）

    saving_address = saving_directory + '/' + file_name + '.xls'  # 文件储存地址
    workbook.save(saving_address)  # 保存工作簿
    print("xls格式表格写入数据成功！")

    return

########################################################################################################################
# 图像保存模块

# 此函数专用于保存利用matplotlib包绘制的图像
def SavingFigure(format='jpg', dpi=600, saving_directory=default_path, file_name='untitled'):
    saving_address = saving_directory + '/' + file_name + '.' + format  # 储存地址
    plt.savefig(saving_address, dpi=dpi, format=format)
    return