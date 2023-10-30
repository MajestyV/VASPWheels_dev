import numpy as np
import pandas as pd
import VaspWheels as vw
import matplotlib.pyplot as plt

if __name__=='__main__':

    # JCPGH1
    data_file = 'D:/Projects/OptoTransition/Experiment/北理工/PL quenching_version20231025/0V.csv'

    data_DataFrame = pd.read_csv(data_file, header=None, sep='\s+')  # 若设置header=0的话，则第一行为列名，从第二行开始读取
    data_array = data_DataFrame.values  # 将DataFrame格式的数据转换为数组
    # data_list.append(data_array)

    #Jumping_degree(data_array,100)
    #plt.ylim(0,200)

    data_filtered = data_array
    for n in range(2):
        data_filtered = vw.Experiment.Removing_jumping_point(data_filtered,threshold=1.1e5)  # 多次循环以去除连续跳变点
    plt.plot(data_filtered[:,0],data_filtered[:,1])

    # 保存数据
    saving_path = 'D:/Projects/OptoTransition/Experiment/北理工/PL quenching_version20231025/0V_test.csv'
    np.savetxt(saving_path, data_filtered, delimiter=",")

    # print(b)