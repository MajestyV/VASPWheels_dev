import numpy as np
import matplotlib.pyplot as plt

from os import path

default_directory = path.dirname(__file__) + '/'  # 设置这个代码文件所在的文件夹为默认读写目录

#class data_recording:
    #''' This class of function is designed for recording data. (这一行的缩进也要跟下一行对齐) '''
    #def __init__(self):
        #self.name = data_recording

    # 用于保存数据的函数
    #def Save_Data(self, saving_directory, file_name, data, sep=' '):
        #file_address = saving_directory + '/' + file_name + '.txt'
        #np.savetxt(file_address, data, delimiter=sep)

    # 用于保存图像的函数
    #def Save_Figure(self, saving_directory, file_name, dpi=600, format=('eps', 'jpg')):
        #for i in format:
            #file_address = saving_directory + '/' + file_name + '.' + str(i)
            #plt.savefig(file_address, dpi=dpi, format=i)



# 用于保存数据的函数
def Save_Data(saving_directory, file_name, data, sep=' '):
    file_address = saving_directory + '/' + file_name + '.txt'
    np.savetxt(file_address, data, delimiter=sep)

# 用于保存图像的函数
def Save_Figure(saving_directory, file_name, dpi=600, format=('eps', 'jpg')):
    for i in format:
        file_address = saving_directory + '/' + file_name + '.' + str(i)
        plt.savefig(file_address, dpi=dpi, format=i)

# 图像保存函数
    def SavingFigure(self,saving_directory,**kwargs):
        filename = kwargs['filename'] if 'filename' in kwargs else 'Untitled'  # 文件名
        format = kwargs['format'] if 'format' in kwargs else 'eps'  # 储存格式
        dpi = kwargs['dpi'] if 'dpi' in kwargs else 600  # 分辨率

        saving_address = saving_directory+filename+'.'+format  # 图像文件要储存到的绝对地址

        plt.savefig(saving_address, dpi=dpi, format=format)

        return