import pandas as pd
import matplotlib.pyplot as plt
import VaspWheels as vw
from MoS2_OptoTransition import QuickVisual

QV = QuickVisual.QuickVisual(x_major=1.5, y_major=0.4)
DR = QuickVisual.data_recording()

if __name__=='__main__':
    data_directory = 'D:/Projects/OptoTransition/Data/Stark_effect/Pentalayer/5'  # 数据文件库

    E_field = ['0.00',
               '0.01','0.02','0.03','0.04','0.05','0.06','0.07','0.08','0.09','0.10',
               '0.11','0.12','0.13','0.14','0.15','0.16','0.17','0.18','0.19','0.20']

    E_bandgap_total = []
    for i in range(len(E_field)):
        data_file = data_directory+'/E_'+E_field[i]+'/EIGENVAL'
        E_bandgap = vw.ElectronicStructure.GetBandgap(data_file)
        E_bandgap_total.append(E_bandgap)

    print(E_bandgap_total)

    ############################################分割线################################################

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