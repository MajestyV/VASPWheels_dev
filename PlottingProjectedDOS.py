import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

data_repository = 'D:/Projects/PhaseTransistor/Data/Simulation/DOS_n_PartialCharge/4_GSE_PDOS/'

E_field = ['0.000', '0.025', '0.075', '0.125', '0.175', '0.225']

atom_list = ['Mo1', 'Mo2', 'Mo3', 'Mo4', 'S1', 'S2', 'S3', 'S4', 'S5', 'S6', 'S7', 'S8']

atom_dict = {'Mo1': [0.3333333429999996, 0.6666666870000029, 0.4310880238549544],
             'Mo2': [0.3333333429999996, 0.6666666870000029, 0.7062630203979339],
             'Mo3': [0.6666666269999979, 0.3333333129999971, 0.2937369796020661],
             'Mo4': [0.6666666269999979, 0.3333333129999971, 0.5689119761450456],
             'S1': [0.6666666870000029, 0.3333333429999996, 0.3954759305142161],
             'S2': [0.6666666870000029, 0.3333333429999996, 0.6706304674638588],
             'S3': [0.3333333129999971, 0.6666666269999979, 0.3293695325361412],
             'S4': [0.3333333129999971, 0.6666666269999979, 0.6045240694857839],
             'S5': [0.3333333129999971, 0.6666666269999979, 0.2580735384661423],
             'S6': [0.3333333129999971, 0.6666666269999979, 0.5332994913558480],
             'S7': [0.6666666870000029, 0.3333333429999996, 0.4667005086441520],
             'S8': [0.6666666870000029, 0.3333333429999996, 0.7419264615338577]}

filename = 'PDOS_SUM_SOC.dat'

# 这个函数利用pandas包读取dat文件中的数据
def GetProjectedDOS(file):
    data = pd.read_csv(file,sep="\s+")  # 以空格作为分隔符，\s匹配任意空白字符，等价于 [\t\n\r\f]
    title = data.columns[0]  # 利用pandas的columns函数获取数据表头
    dimension = data.shape   # 利用pandas的shape函数获取数据的维度，格式为： （行数，列数）
    return data, title, dimension

data_dict = {}  # 创建空字典，所有的数据都将保存在这个字典中
for n in atom_list:
    data_file = data_repository+E_field[5]+'/'+n+'/'+filename
    df,t,dim = GetProjectedDOS(data_file)

    energy = df['#Energy']  # 根据列名取DataFrame中的列数据
    dos = df['tot']

    data_dict[n] = (energy.values.T.tolist(),dos.values.T.tolist())  # 将DataFrame格式数据转换为list格式数据

#print(data_dict)

#data = pd.read_csv(file,sep="\s+")

#title = data.columns[0]  # 利用pandas的columns函数获取数据表头
#dimension = data.shape   # 利用pandas的shape函数获取数据的维度，格式为： （行数，列数）

#energy = data['#Energy'] # 根据列名取列
#dos = data['tot']

#energy = energy.values.T.tolist()  # 将DataFrame格式数据转换为list格式数据
#dos = dos.values.T.tolist()

#plt.plot(energy,dos)
#plt.xlim(-7.5,5)
#plt.ylim(-1,10)

# 利用subplot函数创建组图，并将figure size的信息还有各组图解压分配给各变量
# e.g. f,((ax11,ax12,ax13),(ax21,ax22,ax23)) = plt.subplots(2,3,sharex=True,sharey=True)
f,((ax1,ax2,ax3,ax4,ax5,ax6)) = plt.subplots(1,6,sharey=True)
# Mo1
ax1.plot(data_dict['Mo1'][1],data_dict['Mo1'][0])
ax1.set_xlim(0,5)        # 在subplot中，利用set_xlim函数设置x轴范围
ax1.set_ylim(-7.5,5)     # 在subplot中，利用set_ylim函数设置y轴范围
# Mo2
ax2.plot(data_dict['Mo2'][1],data_dict['Mo2'][0])
ax2.set_xlim(0,5)
ax2.set_ylim(-7.5,5)
# Mo3
ax3.plot(data_dict['Mo3'][1],data_dict['Mo3'][0])
ax3.set_xlim(0,5)
ax3.set_ylim(-7.5,5)
# Mo4
ax4.plot(data_dict['Mo4'][1],data_dict['Mo4'][0])
ax4.set_xlim(0,5)
ax4.set_ylim(-7.5,5)

plt.tight_layout()  #检查坐标轴标签、刻度标签以及标题的部分。自动调整子图参数，使之填充整个图像区域。
plt.show()
print(f)