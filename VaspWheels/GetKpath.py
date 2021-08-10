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
    def GetKpath(self,saving_directory,path,npoints=100):
        kpath = self.Kgenerator(path,npoints)
        KPOINTS = saving_directory+'KPOINTS_ebands'
        f = open(KPOINTS,'w')
        f.write('auto generate\n'+
                str(len(kpath))+'\n'
                'Reciprocal\n')
        for i in range(len(kpath)):
            f.write(str(kpath[i][0])+' '+str(kpath[i][1])+' '+str(kpath[i][2])+' 1\n')
        f.close()
        return

    # This function is written to project the K-path into one dimensional line.
    def ProjectKpath(self,path,npoints=100,**kwargs):
        correction = kwargs['LatticeCorrection'] if 'LatticeCorrection' in kwargs else 'False'  # 这段代码用于晶格修正K空间的尺度
        lattice, parameters, type = kwargs['Lattice'] if 'Lattice' in kwargs else ['Cubic', [1, 1, 1, 90, 90, 90], 'primitive']
        b1,b2,b3 = crystal.Reciprocal_lattice(lattice,parameters,type)
        correction_array = np.array([np.linalg.norm(b1,ord=2),np.linalg.norm(b2,ord=2),np.linalg.norm(b3,ord=2)])

        nnodes = len(path)  # number of K-point nodes in the path
        # print(nnodes)
        kprojection = []
        nodes = []
        kp = 0  # Always setting the origin as starting point
        kprojection.append(kp)
        nodes.append(kp)
        for i in range(nnodes-1):  # n nodes indicating the whole is seperated into n-1 subpaths
            # print(path[i+1],path[i])
            subpath = np.array(path[i+1])-np.array(path[i])
            if correction == 'True':  # 启动晶格修正选项
                subpath = np.multiply(subpath,correction_array)  # np.multiply: 数组对应元素位置相乘
            else:
                pass
            lsubpath = np.linalg.norm(subpath,ord=2)  # 求这段路径的二阶范数，也就是向量的模
            delta = lsubpath/(npoints+1)  # n points seperate the subpath into n+1 sections
            for j in range(npoints):
                kp = kp+delta
                kprojection.append(kp)
            kp = kp+delta  # This is the K-projection position of the nodes except the first node, because npoints do not include the nodes
            kprojection.append(kp)
            nodes.append(kp)

        # kpath.append(path[nnodes - 1])
        return kprojection,nodes

if __name__=='__main__':
    saving_directory = 'D:/OneDrive/OneDrive - The Chinese University of Hong Kong/Desktop/Testing/'
    kpath = Kpath()
    # Gamma-M-K-Gamma-A-L-H-A
    path = [[0,0,0],[0.5,0,0],[1.0/3.0,1.0/3.0,0],[0,0,0],[0,0,0.5],[0.5,0,0.5],[1.0/3.0,1.0/3.0,0.5],[0,0,0.5]]
    #a = kpath.Kgenerator(path,59)
    b = kpath.ProjectKpath(path,59,LatticeCorrection='True',Lattice=['HEX', [3.16, 3.16, 12.9, 90, 90, 120], 'primitive'])
    #print(len(a))
    print(b[0])
    print(b[1])
    #kpath.GetKpath(saving_directory,path,59)

    #LatticeParam = ['HEX', [3.16, 3.16, 12.9, 90, 90, 120], 'primitive']
    #lattice, parameters, type = LatticeParam
    #print(crystal.Reciprocal_lattice(lattice,parameters,type))