import numpy as np
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

########################################################################################################################
# 图像保存模块

# 此函数专用于保存利用matplotlib包绘制的图像
def SavingFigure(format='jpg', dpi=600, saving_directory=default_path, file_name='untitled'):
    saving_address = saving_directory + '/' + file_name + '.' + format  # 储存地址
    plt.savefig(saving_address, dpi=dpi, format=format)
    return