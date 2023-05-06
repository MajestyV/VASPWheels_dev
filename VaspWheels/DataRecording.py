import numpy as np
import matplotlib.pyplot as plt

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