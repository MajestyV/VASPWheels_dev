# This code is written for generating K-point path file for first-principles calculation and analyzing computation results.

import numpy as np
import VaspWheels as vw
from VaspWheels import Crystallography


########################################################################################################################
# KPOINTS文件生成模块：此模块的函数专门用于生成VASP计算所需的KPOINTS文件

# 这个函数可以指定K点列表生成V.A.S.P.计算所需的KPOINTS文件
def GenKPOINTS(saving_address, Kpoints_list):
    file = open(saving_address, 'w')
    file.write('auto generate\n' +     # 写入KPOINTS文件表头
                str(len(Kpoints_list)) + '\n' +
                'Reciprocal\n')
    for i in range(len(Kpoints_list)):  # 根据Kpoints_list将K点一个个写入
        file.write(str(Kpoints_list[i][0])+' '+str(Kpoints_list[i][1])+' '+str(Kpoints_list[i][2])+' 1\n')
    file.close()
    return

# 此函数可以通过指定端点（转折点）生成完整的K点路径
# This function is designed to generate the K-points trajectory.
# Example input: path=[[0,0,0],[0.5,0,0],[0.5,0.5,0],[0.5,0.5,0.5],[0,0,0]], npoints is the number of points between two neighboring nodes in the path
def GenerateKpath(Knodes,npoints=100):
    nnodes = len(Knodes)  # number of K-point nodes in the path
    Kpath = []
    for i in range(nnodes-1):  # n nodes indicating the whole is seperated into n-1 subpaths
        subpath = np.array(Knodes[i+1])-np.array(Knodes[i])
        delta = subpath/(npoints+1)  # n points seperate the subpath into n+1 sections
        Kpath.append(Knodes[i])
        for j in range(npoints):
            k = np.array(Knodes[i])+(j+1)*delta
            Kpath.append(list(k))

    Kpath.append(Knodes[nnodes-1])
    return Kpath

# 这个函数可以通过指定高对称K点端点生成K点路径文件，专用于能带计算（当然，对于VASP5以上用户，强烈建议直接用vasp自带的linemode）
# This function is written to generate KPOINTS file for electronic dispersion calculation.
def GetKpath(saving_address,nodes,npoints=100):
    Kpath = GenerateKpath(nodes,npoints)
    KPOINTS = saving_address
    file = open(KPOINTS,'w')
    file.write('auto generate\n'+  # 写入KPOINTS文件表头
                str(len(Kpath))+'\n'
                'Reciprocal\n')
    for i in range(len(Kpath)):
        file.write(str(Kpath[i][0])+' '+str(Kpath[i][1])+' '+str(Kpath[i][2])+' 1\n')
    file.close()
    return

########################################################################################################################

# 此函数可以将三维的K点路径投影为K点路程
# K点路径（Kpath）实际上是一系列的向量坐标，想象一个点沿这个路径不断地走，那么它走过的路程将不断增加
# 将沿这个路程计算得到的能量值展开，我们就得到了经常能看到的能带图
def ProjectKpath(Kpath,num_segments,lattice_param=('Cubic', [1, 1, 1, 90, 90, 90], 'primitive')):
    lattice, parameters, type = lattice_param  # 输入晶格常数，默认为立方单位晶格，即不作任何的晶格修正
    b1,b2,b3 = vw.Crystallography.Reciprocal_lattice(lattice,parameters,type)  # 计算倒空间基矢
    # 通过倒空间基矢的长度，对K点路程进行晶格修正
    scaling = np.array([np.linalg.norm(b1,ord=2),np.linalg.norm(b2,ord=2),np.linalg.norm(b3,ord=2)])

    Kpath = np.array(Kpath)  # 将K点路径转换为数组，防止后面出错
    num_kpoints = len(Kpath)  # K点路径中的K点数目

    K_distance = 0.0  # K点路程的初始值为0
    Kpath_projected = [K_distance]  # 记录每一个路程点
    for i in range(num_kpoints-1):
        # 因为有些路径向着负方向，所以要取绝对值
        K_distance = K_distance+abs(np.dot((Kpath[i+1]-Kpath[i]),scaling))
        Kpath_projected.append(K_distance)

    # 接下来，我们将K点路径转折点对应的路程端点取出，以在能带图上分块，方便分析
    # inter = int((num_kpoints-1)/num_segments)  # 总点数 = 分段数*间隔点数+1  -- for old version of VaspWheels
    # Knodes_projected = Kpath_projected[0:num_kpoints:inter]  # K点路程端点

    inter = int((num_kpoints)/num_segments)  # 总点数 = 分段数*间隔点数  -- for linemode K-path
    Knodes_projected = [Kpath_projected[0]]+[Kpath_projected[inter*i-1] for i in range(1,num_segments+1)]  # K点路程端点

    return Kpath_projected, Knodes_projected