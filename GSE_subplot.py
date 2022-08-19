import re
import codecs
import numpy as np
import matplotlib.pyplot as plt
from VaspWheels import GetEbands
from VaspWheels import GetKpath

GetE = GetEbands.Ebands()
GetK = GetKpath.Kpath()

# 此函数可以用于在列表中定位特定元素的序号引索
def GetIndex(element,target_list):
    return [index for (index,value) in enumerate(target_list) if value == element]

# 此函数可以用于从计算结果中提取费米面
def GetFermiEnergy(Markdown):  # Markdown文件中应记载着准确的费米能级
    pattern = re.compile(r'-?\d+\.?\d+')  # 匹配浮点数的正则表达式
    f = codecs.open(Markdown, 'rb', 'utf-8', 'ignore')
    line = f.readline()
    energy = pattern.findall(line)
    fermi_energy = float(energy[0])
    return fermi_energy

# 此函数可以用于费米面调零
def ShiftFermi(energy, fermi_energy):
    nbands = len(energy)  # number of bands
    nkpoints = len(energy[0])  # number of k points calculated
    shifted_energy = [[] for n in range(nbands)]
    for i in range(nbands):
        for j in range(nkpoints):
            shifted_energy[i].append(energy[i][j]-fermi_energy)
    return shifted_energy

# 此函数可以用于能带截取
def InterceptingEbands(EIGENVAL,InterceptedKpath,fermi_energy):
    # 提取能带计算结果以及各种参数
    bands = GetE.GetData(EIGENVAL)
    nbands = bands['number']  # 提取能带总数
    kpath = bands['kpath']  # K点路径
    print(kpath)
    energy = bands['energy']  # 能带具体的能量值
    energy = ShiftFermi(energy, fermi_energy)  # 进行费米面调零

    starting_point, end_point = InterceptedKpath  # 从InterceptedKpath中提取起点跟终点
    starting_index = kpath.index(starting_point)
    #end_index = kpath.index(end_point)            # 终点的序号
    end_index = GetIndex(end_point,kpath)[1]

    print(starting_index,end_index)

    # 对能带进行切片
    InterceptedEbands = []
    for i in range(nbands):
        InterceptedEbands.append(energy[i][starting_index:end_index+1])

    K_projected = np.linspace(0,100,end_index-starting_index+1)

    return K_projected, InterceptedEbands, nbands

main_dir = 'D:/Projects/PhaseTransistor/Data/Simulation/GSE/OPTCELL/4_D3BJ_GSE_OPTCELL_1'
data_list = ['0.075', '0.150','0.225']

grid = plt.GridSpec()
# plt.figure(figsize=(5,5))  # 控制图片大小

fig, axes = plt.subplots(1,4,sharey='row')  # 创建网格多子图

for n in data_list:
    data_EIGENVAL = main_dir+'/'+n+'/EIGENVAL'
    data_Markdown = main_dir+'/'+n+'/Markdown_SCF' # 这个文件记载着准确的费米能级

    x,y, num_y = InterceptingEbands(data_EIGENVAL,[[0.3333333,0.3333333,0],[0,0,0]],GetFermiEnergy(data_Markdown))

    for i in range(num_y):
        axes[data_list.index(n)].plot(x, y[i])

plt.ylim(-2,5)

plt.show()