import pandas as pd
from VaspWheels import AnalyzeBandgap

AB = AnalyzeBandgap.Bandgap()  # 调用AnalyzeBandgap模块

###################################################################################################################
# 定义函数方便进行数据处理

# 此函数可以将数组形式的数据序列保存为csv文件
def SaveData(saving_directory, data, index=False, header=False, **kwargs):
    ncol = len(data)  # 数据的列数

    keys = kwargs['keys'] if 'keys' in kwargs else ['col' + str(i) for i in range(ncol)]  # 数据字典的key
    KeyValue_list = [(keys[i], data[i]) for i in range(ncol)]  # 创建键值对元组列表
    data_dict = dict(KeyValue_list)  # 将二元组列表转换为字典

    data_DataFrame = pd.DataFrame(data_dict)  # 利用pandas的DataFrame函数将字典转换为DataFrame格式的数据

    # index表示设定是否需要行索引，设定为FALSE表明不需要，就不会生成新的行索引
    # header表明是否需要列索引，设定为True（默认为False）表明需要，那么data_DataFrame中的列标签就会保存
    data_DataFrame.to_csv(saving_directory, index=index, header=header)

    return
###################################################################################################################
# 从计算结果中提取数据

# 存放不同层数的计算结果的文件夹的绝对地址的字典
# Monolayer
#Main_directory_negative = 'D:/Projects/PhaseTransistor/Data/Simulation/GSE/1/1_D3BJ_GSE_m1_221013/'  # negative
#Main_directory_positive = 'D:/Projects/PhaseTransistor/Data/Simulation/GSE/1/1_D3BJ_GSE_1_221013/'  # positive
# Bilayer
# Main_directory_negative = 'D:/Projects/PhaseTransistor/Data/Simulation/GSE/2/2_D3BJ_GSE_m1/'  # negative
# Main_directory_positive = 'D:/Projects/PhaseTransistor/Data/Simulation/GSE/2/2_D3BJ_GSE_1/'  # positive
# Trilayer
# Main_directory_negative = 'D:/Projects/PhaseTransistor/Data/Simulation/GSE/3/3_D3BJ_GSE_m1/'  # negative
# Main_directory_positive = 'D:/Projects/PhaseTransistor/Data/Simulation/GSE/3/3_D3BJ_GSE_1/'  # positive
# Quadralayer
# Main_directory_negative = 'D:/Projects/PhaseTransistor/Data/Simulation/GSE/4/4_D3BJ_GSE_m1_more_bands/'  # negative
# Main_directory_positive = 'D:/Projects/PhaseTransistor/Data/Simulation/GSE/4/4_D3BJ_GSE_1_more_bands/'  # positive
# Pentalayer
Main_directory_negative = 'D:/Projects/PhaseTransistor/Data/Simulation/GSE/5/5_D3BJ_GSE_m1/'  # negative
Main_directory_positive = 'D:/Projects/PhaseTransistor/Data/Simulation/GSE/5/5_D3BJ_GSE_1/'  # positive

# 在不同层数的计算结果的文件夹中，存放数据的文件夹；同时也恰好时电场强度，单位为V/Angstrom
# For negative part of monolayer and bilayer
#Efield_negative = ['m0.550','m0.525','m0.500','m0.475','m0.450','m0.425','m0.400','m0.375','m0.350','m0.325','m0.300',
                   #'m0.275','m0.250','m0.225','m0.200','m0.175','m0.150','m0.125','m0.100','m0.075','m0.050','m0.025']
# For positive part of monolayer and bilayer
#Efield_positive = ['0.000','0.025','0.050','0.075','0.100','0.125','0.150','0.175','0.200','0.225','0.250','0.275',
                   #'0.300','0.325','0.350','0.375','0.400','0.425','0.450','0.475','0.500','0.525','0.550']
# For negative part of trilayer
#Efield_negative = ['m0.350','m0.325','m0.300','m0.275','m0.250','m0.225','m0.200','m0.175','m0.150','m0.125',
                   #'m0.100','m0.075','m0.050','m0.025']
# For positive part of trilayer
#Efield_positive = ['0.000','0.025','0.050','0.075','0.100','0.125','0.150','0.175','0.200','0.225','0.250',
                   #'0.275','0.300','0.325','0.350']
# For negative part of quadralayer and pentalayer
Efield_negative = ['m0.300','m0.275','m0.250','m0.225','m0.200','m0.175','m0.150','m0.125','m0.100','m0.075','m0.050','m0.025']
# For positive part of quadralayer and pentalayer
Efield_positive = ['0.000','0.025','0.050','0.075','0.100','0.125','0.150','0.175','0.200','0.225','0.250','0.275','0.300']


Bandgap, ValenceMax, ConductionMin, Extremum_POS = [[],[],[],[]]
# 先读取负电场
for n in Efield_negative:
    data_directory = Main_directory_negative+n+'/'  # 存放画能带图所需的数据文件的绝对地址
    EIGENVAL = data_directory+'EIGENVAL'  # EIGENVAL文件的绝对地址

    Eg, Ev_max, Ec_min, pos = AB.AnalyzeBandgap(EIGENVAL,mode='Occupation')
    Bandgap.append(Eg)
    ValenceMax.append(Ev_max)
    ConductionMin.append(Ec_min)
    Extremum_POS.append(pos)
# 再读取正电场
for n in Efield_positive:
    data_directory = Main_directory_positive+n+'/'  # 存放画能带图所需的数据文件的绝对地址
    EIGENVAL = data_directory+'EIGENVAL'  # EIGENVAL文件的绝对地址

    Eg, Ev_max, Ec_min, pos = AB.AnalyzeBandgap(EIGENVAL,mode='Occupation')
    Bandgap.append(Eg)
    ValenceMax.append(Ev_max)
    ConductionMin.append(Ec_min)
    Extremum_POS.append(pos)

#print(Bandgap)        # 带隙
#print(ValenceMax)     # 价带顶
#print(ConductionMin)  # 导带底
#print(Extremum_POS)   # 极值点位置（若很接近，则是直接带隙；否则为间接带隙）

#####################################################################################################################
# 保存数据

saving_directory = 'D:/Projects/PhaseTransistor/Data/Simulation/GSE/GSE数据总结/Occupation/5_pentalayer.csv'

SaveData(saving_directory,[Bandgap,ValenceMax,ConductionMin,Extremum_POS])