# This code is designed for providing useful functions in processing experimental data.

import numpy as np
import matplotlib.pyplot as plt

########################################################################################################################
# 跳变点去除模块，此模块专门针对形如[[x0,y0],[x1,y1], ... [xn,yn]]的二维数组
# 详情请参考：基于python的一种异常值快速判读剔除方法：“跳跃度”法（https://blog.csdn.net/weixin_45719141/article/details/115938456）

# 计算数据的跳跃值分布
def Jumping_degree(data,num_bins=30):
    data = np.array(data)
    x, y = (data[:,0],data[:,1])
    data_length = len(x)
    jump_deg = []
    for i in range(data_length-1):  # 由于采用前微分的形式计算跳跃度，所以循环长度要减一
        jump_deg.append((y[i+1]-y[i])/(x[i+1]-x[i]))  # 计算斜率（即数据点之间的跳跃度）

    # 可视化数据，方便分析
    plt.hist(jump_deg,num_bins)
    plt.xlim(min(jump_deg),max(jump_deg))

    return jump_deg

# 通过设定阈值去除跳变点
def Removing_jumping_point(data,threshold):
    data = np.array(data)
    x, y = (data[:,0],data[:,1])
    data_length = len(x)
    data_filtered = []
    for i in range(data_length-1):  # 由于采用前微分的形式计算跳跃度，所以循环长度要减一
        slope = (y[i+1]-y[i])/(x[i+1]-x[i])  # 计算斜率（即数据点之间的跳跃度）
        if abs(slope) >= threshold:  # 如果斜率的绝对值超过阈值，则去除
            pass
        else:
            data_filtered.append([x[i],y[i]])
    data_filtered.append([x[data_length-1],y[data_length-1]])  # 补充回最后一个点
    return np.array(data_filtered)

########################################################################################################################
# 数据处理模块，详情请参考：
# python 数据、曲线平滑处理——方法总结（https://blog.csdn.net/weixin_42782150/article/details/107176500）

# 滑动平均滤波，data应为一维数组，而windowsize应为整型
def Moving_average(data,windowsize,mode='same'):
    window = np.ones(int(windowsize))/float(windowsize)
    data_filtered = np.convolve(data,window,mode=mode)
    return data_filtered

# if __name__=='__main__':
    # JCPGH1
    #data_file = 'D:/Projects/OptoTransition/Experiment/北理工/PL quenching_version20231025/0V.csv'

    #data_DataFrame = pd.read_csv(data_file, header=None, sep='\s+')  # 若设置header=0的话，则第一行为列名，从第二行开始读取
    #data_array = data_DataFrame.values  # 将DataFrame格式的数据转换为数组
    # data_list.append(data_array)

    #Jumping_degree(data_array,100)
    #plt.ylim(0,200)

    #data_filtered = Removing_jumping_point(data_array,threshold=2e5)
    #plt.plot(data_filtered[:,0],data_filtered[:,1])

    # print(b)