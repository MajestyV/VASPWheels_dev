import pandas as pd
import matplotlib.pyplot as plt
from MoS2_OptoTransition import QuickVisual

QV = QuickVisual.QuickVisual(x_major=1.5, y_major=0.4)
DR = QuickVisual.data_recording()

if __name__=='__main__':
    # data_directory = 'D:/Projects/OptoTransition/Data/ElectricField/TOTEN'  # JCPGH1
    data_directory = 'D:/Projects/OptoTransition/Data/Total/GSE/2'  # MMW502

    file_list = ['GSE_2.txt','GSE_2_SYM.txt',
                 'GSE_2_SOC.txt','GSE_2_SOC_SYM.txt']

    data_total = []
    for file in file_list:
        file_address = data_directory+'/'+file
        data_DataFrame = pd.read_csv(file_address,header=None,sep=' ')
        data_total.append(data_DataFrame.values)

    # 画图模块
    # color = ["#6495ED", "#F08080"]
    color = ['#4878d0', '#d65f5f', '#ee854a', '#6acc64']
    symbol = ['s','o','^','p']
    label = ['no SOC + no sym.', 'no SOC + sym.', 'SOC + no sym.', 'SOC + sym.']

    for i in [0,1,2,3]:
        indexing = i
        x = data_total[i][:,0]
        y = data_total[i][:,1]
        plt.plot(x,y,c=color[indexing],marker=symbol[indexing],label=label[indexing])

    plt.xlim(0,5.5)
    plt.ylim(0,1.3)

    plt.xlabel('Electric field (V/nm)')
    plt.ylabel('Band gap (eV)')
    plt.legend(frameon=False)

    # 数据保存
    # print(Bandgap)
    saving_directory = 'D:/OneDrive/OneDrive - The Chinese University of Hong Kong/Desktop/Test'
    DR.Save_Figure(saving_directory, 'GSE_2')