# This code is designed for analyzing elemental distribution data gained from electron microscopic characterizations.
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator

class EDX:
    ''' This class of function is designed to analyze EDX data. '''
    def __init__(self,data,L,W,N,mode=1):
        self.L = L
        self.W = W
        self.N = N
        # self.intensity = np.empty((L,W,N,1))  # 加入判断，到底数据有没有预处理
        self.intensity = data

        # 检测模块，判断是点扫，线扫还是面扫

    # 此函数可以从EDX信号强度数据中计算出原子比例（atomic percentage）
    def Calculate_AtomicPercentage(self):
        atomic_percentage = np.empty((self.L,self.W,self.N))
        for i in range(self.L):
            for j in range(self.W):
                elemental_sum = sum(self.intensity[i,j])  # 坐标 R=(i,j) 处的所有元素信号强度求和
                for k in range(self.N):  # 遍历所有元素
                    atomic_percentage[i,j,k] = float(self.intensity[i,j,k])/float(elemental_sum)  # 转换为浮点数，防止运算出错
        return atomic_percentage

if __name__=='__main__':
    # Guangzhou
    data_directory = 'D:/PhD_research/OptoTransition/Experiment/FIB/Raw data/20230929-EDX line profile'

    element_list = ['Pt', 'Au', 'C', 'Mo', 'Si', 'In']
    num_atom = len(element_list)

    data_list = []
    for n in element_list:
        data_file = data_directory+'/'+n+'.txt'
        data_DataFrame = pd.read_csv(data_file, header=None, sep='\s+')  # 若设置header=0的话，则第一行为列名，从第二行开始读取
        data_array = data_DataFrame.values  # 将DataFrame格式的数据转换为数组
        data_list.append(data_array)
    data_total = np.array(data_list)  # 汇总完的数据
    # print(data_total)

    # 对汇总的数据进行重整
    W = len(data_total[0])
    print(W)
    data_EDX =np.empty((1,W,num_atom))
    for i in range(num_atom):
        for j in range(W):
            data_EDX[0,j,i] = data_total[i][j][1]
            # data_EDX[0,]
            # data_EDX[0,i,j] = data_total[0][j][i]

    print(data_EDX)

    edx = EDX(data_EDX,1,W,num_atom)
    atomic_percentage = edx.Calculate_AtomicPercentage()

    print(atomic_percentage)


    # 画图模块
    plt.rcParams.update({'xtick.direction': 'in', 'ytick.direction': 'in'})  # 设置x轴和y轴刻度线方向向内

    ax = plt.subplot(111)  # 创建图例对象（注意有些参数（比如刻度）一般都在ax中设置,不在plot中设置）

    # 设置主刻度
    x_major_locator = MultipleLocator(0.5)  # 将x主刻度标签设置为x_major_tick的倍数
    y_major_locator = MultipleLocator(600)  # 将y主刻度标签设置为y_major_tick的倍数
    ax.xaxis.set_major_locator(x_major_locator)
    ax.yaxis.set_major_locator(y_major_locator)


    width = data_total[0,:,0]*1e9
    # print(width)
    for i in range(num_atom):
        plt.plot(atomic_percentage[0,:,i],-width)

    plt.xlim(-0.03,1)
    plt.ylim(-1801,0)
