# This code is designed for providing useful functions in processing experimental data.

import numpy as np
import pandas as pd

########################################################################################################################
# 跳变点去除模块，详情请参考：
# 基于python的一种异常值快速判读剔除方法：“跳跃度”法（https://blog.csdn.net/weixin_45719141/article/details/115938456）

# 求跳跃值函数
def Jumping_degree(data):
    jump_deg = []
    for i in range(len(data)-1):
        jump_deg.append(data[i+1]/data[i])
    return jump_deg

#



#test_data.sort(reverse=True)#按降序排列

#print(test_data)
#print(jumdeg(test_data))



########################################################################################################################
# 数据处理模块，详情请参考：
# python 数据、曲线平滑处理——方法总结（https://blog.csdn.net/weixin_42782150/article/details/107176500）

# 滑动平均滤波，data应为一维数组，而windowsize应为整型
def Moving_average(data,windowsize,mode='same'):
    window = np.ones(int(windowsize))/float(windowsize)
    data_filtered = np.convolve(data,window,mode=mode)
    return data_filtered

if __name__=='__main__':
    # JCPGH1
    data_file = 'D:/Projects/OptoTransition/Experiment/北理工/PL quenching_version20231025/0V.csv'

    data_DataFrame = pd.read_csv(data_file, header=None, sep='\s+')  # 若设置header=0的话，则第一行为列名，从第二行开始读取
    data_array = data_DataFrame.values  # 将DataFrame格式的数据转换为数组
    # data_list.append(data_array)


    a = Jumping_degree(data_array[:,1])
    b = a.sort(reverse=True)

    print(b)