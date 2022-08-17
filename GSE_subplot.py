import numpy as np
import matplotlib.pyplot as plt
from VaspWheels import GetEbands
from VaspWheels import GetKpath

GetE = GetEbands.Ebands()
GetK = GetKpath.Kpath()

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
    nkpoints_total = bands['num kpoints']  # 提取K点总数
    nnodes = len(Kpath)  # 高对称点数
    npoints = int((nkpoints_total - nnodes) / (nnodes - 1))  # 两个高对称点中间的取点数 = (K点总数-高对称点数)/(高对称点数-1)

    energy = bands['energy']  # 能带具体的能量值
    energy = ShiftFermi(energy, fermi_energy)  # 进行费米面调零

    starting_point =

    # 提取K点总路径
    # 确定K点路径（X轴）
    correction = kwargs['LatticeCorrection'] if 'LatticeCorrection' in kwargs else 'False'  # 晶格修正选项
    lattice = kwargs['Lattice'] if 'Lattice' in kwargs else ['Cubic', [1, 1, 1, 90, 90, 90], 'primitive']
    k, knodes = GetK.ProjectKpath(Kpath, npoints, LatticeCorrection=correction, Lattice=lattice)  # 生成投影到一维的K点路径

# plt.figure(figsize=(5,5))  # 控制图片大小

fig, axes = plt.subplots(1,4,sharey='row')  # 创建网格多子图

plt.show()