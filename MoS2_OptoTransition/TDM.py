########################################################################################################################
# 模块调用
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from VaspWheels import GeneralAnalyzer,GetKpath,GetElectronicBands,Visualization,VisualizeBands

# GA = GeneralAnalyzer.functions()  # 调用GeneralAnalyzer模块（通用数据分析包）
GK = GetKpath.vasp()              # 调用GetKpath模块（可以获取K点路径）
GE = GetElectronicBands.vasp()    # 调用GetElectronicBands模块（可以获取能带数据）
VI = Visualization.plot()         # 调用Visualization模块（可视化基础包）
VB = VisualizeBands.plot_bands()  # 调用VisualizeBands模块（能带可视化专用包）

class TDM:
    ''' TDM - short for Transition Dipole Moment '''
    def __init__(self):
        self.name = TDM

        # 以字典形式记录的计算结果所在的主目录
        data_directory = {'MMW502': 'D:/Projects/OptoTransition/Data',  # 办公室电脑
                          'JCPGH1': 'D:/Projects/OptoTransition/Data',  # 宿舍电脑
                          'Macbook': '/Users/liusongwei/Desktop/OptoTransition/Data',
                          'Zhuhai': 'D:/PhD_research\OptoTransition/Data'}  # Macbook

    def GetTDM(self,data_file):
        data_DataFrame = pd.read_csv(data_file, header=0, sep='\s+')  # pandas利用读取数据文件中的数据，返回的数据格式为pandas包专有的DataFrame格式
        data_array = data_DataFrame.values  # 将数据从DataFrame格式转换为数组格式
        return data_array

    def GetTDM_batch(self,file_list):
        data_dict = {}
        for i in file_list:
            data_dict[i] = self.GetTDM(i)
        return data_dict

if __name__=='__main__':
    # 以字典形式记录的计算结果所在的主目录
    data_directory = {'MMW502': 'D:/Projects/OptoTransition/Data',  # 办公室电脑
                      'JCPGH1': 'D:/Projects/OptoTransition/Data',  # 宿舍电脑
                      'Macbook': '/Users/liusongwei/Desktop/OptoTransition/Data',  # Macbook
                      'Zhuhai': 'D:/PhD_research/OptoTransition/Data'}  # 珠海电脑
    val_band_index = [21,22,23,24]  # valence band index
    con_band_index = [25,26,27,28]  # conduction band index

    Efield = 'E_0.525'

    data_file = data_directory['Zhuhai']+'/TDM/2-layer/GSE_Bilayer_TDM/'+Efield+'/'+str(val_band_index[3])+'-'+str(con_band_index[0])+'/TDM.dat'

    data_file_list = [data_directory['Zhuhai']+'/TDM/2-layer/GSE_Bilayer_TDM/'+Efield+'/'+str(val_band_index[i])+'-'+str(con_band_index[j])+'/TDM.dat'
                       for i in range(len(val_band_index)) for j in range(len(con_band_index))]

    TDM = TDM()
    data = TDM.GetTDM(data_file)
    data_dict = TDM.GetTDM_batch(data_file_list)

    # print(data_DF)
    # print(np.array(data_DF))

    Kpath_origin, Kpath_destination = [min(data[:, 0]), max(data[:, 0])]  # 获取投影K点路径的起点跟终点

    for file in data_file_list:
        data = data_dict[file]
        plt.plot(data[:,0],data[:,1])
        #Kpath_projected, TDM = (data[i][:,0],data[i][:,1])
        #plt.plot(Kpath_projected,TDM)

    # plt.plot(data[:,0],data[:,1])

    plt.xlim(Kpath_origin,Kpath_destination)
    plt.ylim(0,400)
    plt.vlines(1.15113,0,500)
    plt.vlines(1.81573,0,500)

    plt.show()