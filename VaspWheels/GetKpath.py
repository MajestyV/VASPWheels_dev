# This code is written for generating K-point path file for first-principles calculation and analyzing computation results.

import numpy as np
from VaspWheels import Crystallography

crystal = Crystallography.crystal()

class vasp:
    def __init__(self):
        self.name = vasp

    ##############################################################################################################
    # 倒易空间（K空间）相关模块（功能包括K空间长度计算，K点路径生成等）

    # 此函数可以通过正（实）空间基矢计算倒易空间基矢
    def CalculateReciprocalLattice(self,real_lattice):
        real_lattice = np.array(real_lattice)  # 确保输入正空间基矢数据为数组形式
        a1, a2, a3 = real_lattice

        volume = np.dot(a1,np.cross(a2, a3))   # 晶胞的体积，后面计算基矢时会用到

        pi = np.pi  # 圆周率
        b1 = (2.0*pi/volume)*np.cross(a2,a3)   # b1 = 2*pi*(a2xa3)/[a1·(a2xa3)]
        b2 = (2.0*pi/volume)*np.cross(a3,a1)   # b2 = 2*pi*(a3xa1)/[a1·(a2xa3)]
        b3 = (2.0*pi/volume)*np.cross(a1,a2)   # b3 = 2*pi*(a1xa2)/[a1·(a2xa3)]

        return np.array([b1, b2, b3])

    # 这个函数可以根据输入的倒格矢计算K空间中任意两点的距离，单位为Å^{-1}
    def Length(self, origin, destination, reciprocal_lattice):
        x, y, z = reciprocal_lattice                   # 倒格矢在正交直角坐标系上的表示，用于计算K空间中向量的长度
        input = [x, y, z, origin, destination]
        input_reformed = [np.array(n) for n in input]  # 批量将所有输入数据转换成数组，防止后续计算出错
        x, y, z, origin, destination = input_reformed  # 将转换后的数据从input_reform中解压出来

        direction = destination - origin  # 计算K空间坐标（布里渊区分数坐标）下由origin（起点）指向destination（终点）的方向向量
        # 计算方向向量在正交直角坐标系下的坐标（投影）
        direction_projected = direction[0]*x+direction[1]*y+direction[2]*z

        length = np.linalg.norm(direction_projected, ord=2)  # 向量的二范数即模长

        return length

    # 此函数可以通过指定端点（转折点）生成完整的K点路径
    # This function is designed to generate the K-points trajectory.
    # Example input: path=[[0,0,0],[0.5,0,0],[0.5,0.5,0],[0.5,0.5,0.5],[0,0,0]], npoints is the number of points between two neighboring nodes in the path
    def GenerateKpath(self,Knodes,npoints=100):
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

    # 此函数可以通过指定起点，方向，步数以及步长来获取一系列的K点路径段
    # 适用于计算电子能带的迁移率，声子能带的声速等需要获取指定能谷或能峰并对能量面进行计算（如求导数，曲率，散度，以及旋度等）的场景
    def GenerateKpath_segment(self, origin_array, destination_array, num_step, step_length, reciprocal_lattice):  # 大修
        x, y, z = reciprocal_lattice                   # 倒格矢在正交直角坐标系上的表示，用于计算K空间中向量的长度
        input = [x, y, z, origin_array, destination_array]
        input_reformed = [np.array(n) for n in input]  # 批量将所有输入数据转换成数组，防止后续计算出错
        x, y, z, origin_array, destination_array = input_reformed  # 将转换后的数据从input_reform中解压出来
        num_segment = len(origin_array)                # K点路径段的段数

        Kpoints_total = []
        for i in range(num_segment):
            origin = origin_array[i]
            destination = destination_array[i]

            direction = destination - origin  # 计算起点指向终点的方向向量
            length = self.Length(origin, destination, reciprocal_lattice)  # 计算方向向量（direction）的长度
            dlength = (num_step-1)*step_length
            interpolating_destination = origin + (dlength/length)*direction  # 通过step_length/length计算出插值的终点
            # 应注意，如果要计算电子或者空穴的有效质量，step_length的长度通常在0.01-0.02 Å左右（当然，越密越好，不过要算的点就多了）
            step_vec = (interpolating_destination-origin)/(num_step-1)  # 通过插点数num_point计算出插点的间隔量d_vec

            Kpoint_segment = []
            Kpoint = origin  # 定义初始值，即为这段路径（segment）的起点（origin）
            for j in range(num_step):
                Kpoint_segment.append(Kpoint)
                Kpoint = Kpoint+step_vec  # 每跑一个循环增加一个d_vec向量

            Kpoints_total = Kpoints_total+Kpoint_segment  # 将每一段K点路径段的K点列表串接

        return Kpoints_total

    ##############################################################################################################
    # KPOINTS文件生成模块

    # 这个函数可以指定K点列表生成V.A.S.P.计算所需的KPOINTS文件
    def GenKPOINTS(self, saving_address, Kpoints_list):
        file = open(saving_address, 'w')
        file.write('auto generate\n' +     # 写入KPOINTS文件表头
                   str(len(Kpoints_list)) + '\n' +
                   'Reciprocal\n')
        for i in range(len(Kpoints_list)):  # 根据Kpoints_list将K点一个个写入
            file.write(str(Kpoints_list[i][0])+' '+str(Kpoints_list[i][1])+' '+str(Kpoints_list[i][2])+' 1\n')
        file.close()
        return

    # This function is written to generate KPOINTS file for electronic dispersion calculation.
    def GetKpath(self,saving_address,nodes,npoints=100):
        Kpath = self.GenerateKpath(nodes,npoints)
        KPOINTS = saving_address
        file = open(KPOINTS,'w')
        file.write('auto generate\n'+  # 写入KPOINTS文件表头
                   str(len(Kpath))+'\n'
                   'Reciprocal\n')
        for i in range(len(Kpath)):
            file.write(str(Kpath[i][0])+' '+str(Kpath[i][1])+' '+str(Kpath[i][2])+' 1\n')
        file.close()
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
    kpath = vasp()
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