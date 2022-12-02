# This code is written for generating K-point path file for first-principles calculation and analyzing computation results.

import numpy as np
from VaspWheels import Crystallography

crystal = Crystallography.Crystal()

class Kpath:
    def __init__(self):
        self.name = Kpath

    # This function is designed to generate the K-points trajectory.
    # Example input: path=[[0,0,0],[0.5,0,0],[0.5,0.5,0],[0.5,0.5,0.5],[0,0,0]], npoints is the number of points between two neighboring nodes in the path
    def Kgenerator(self,path,npoints=100):
        nnodes = len(path)  # number of K-point nodes in the path
        #print(nnodes)
        kpath = []
        for i in range(nnodes-1):  # n nodes indicating the whole is seperated into n-1 subpaths
            #print(path[i+1],path[i])
            subpath = np.array(path[i+1])-np.array(path[i])
            delta = subpath/(npoints+1)  # n points seperate the subpath into n+1 sections
            kpath.append(path[i])
            for j in range(npoints):
                k = np.array(path[i])+(j+1)*delta
                kpath.append(list(k))

        kpath.append(path[nnodes-1])
        return kpath

    # This function is written to generate KPOINTS file for electronic dispersion calculation.
    def GetKpath(self,saving_address,nodes,npoints=100):
        kpath = self.Kgenerator(nodes,npoints)
        KPOINTS = saving_address
        f = open(KPOINTS,'w')
        f.write('auto generate\n'+
                str(len(kpath))+'\n'
                'Reciprocal\n')
        for i in range(len(kpath)):
            f.write(str(kpath[i][0])+' '+str(kpath[i][1])+' '+str(kpath[i][2])+' 1\n')
        f.close()
        return

    # 此函数可以将三维的K点路径投影为K点路程
    # K点路径（Kpath）实际上是一系列的向量坐标，想象一个点沿这个路径不断地走，那么它走过的路程将不断增加
    # 将沿这个路程计算得到的能量值展开，我们就得到了经常能看到的能带图
    def ProjectKpath(self,Kpath,num_segments,**kwargs):
        # 输入晶格常数，默认为立方单位晶格，即不作任何的晶格修正
        lattice, parameters, type = kwargs['Lattice'] if 'Lattice' in kwargs else ['Cubic', [1, 1, 1, 90, 90, 90], 'primitive']
        b1,b2,b3 = crystal.Reciprocal_lattice(lattice,parameters,type)  # 计算倒空间基矢
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
        inter = int((num_kpoints-1)/num_segments)  # 总点数 = 分段数*间隔点数+1
        Knodes_projected = Kpath_projected[0:num_kpoints:inter]  # K点路程端点

        return Kpath_projected, Knodes_projected

if __name__=='__main__':
    #saving_directory = 'D:/OneDrive/OneDrive - The Chinese University of Hong Kong/Desktop/Kpoints_ebands'
    saving_directory = 'D:/Projects/PhaseTransistor/Data/Simulation/Phase/input_files/K-path_ORT_1'
    kpath = Kpath()
    # Gamma-M-K-Gamma-A-L-H-A
    # path = [[0, 0, 0], [0.5, 0, 0], [1.0 / 3.0, 1.0 / 3.0, 0], [0, 0, 0], [0,0,1/2.0], [1/2.0,0,1/2.0], [1/3.0, 1/3.0, 1/2.0], [0,0,1/2.0]]
    # Gamma-X-S-Y-Gamma-A
    path = [[0, 0, 0], [0, 0.5, 0], [0.5, 0.5, 0], [0.5, 0, 0], [0, 0, 0], [0.5, 0.5, 0]]
    #a = kpath.Kgenerator(path,59)
    b = kpath.ProjectKpath(path,59,LatticeCorrection='True',Lattice=['ORT', [3.16, 5.47, 12.9, 90, 90, 90], 'unitcell'])
    #print(len(a))
    print(b[0])
    print(b[1])
    kpath.GetKpath(saving_directory,path,99)
    #LatticeParam = ['HEX', [3.16, 3.16, 12.9, 90, 90, 120], 'primitive']
    #lattice, parameters, type = LatticeParam
    #print(crystal.Reciprocal_lattice(lattice,parameters,type))