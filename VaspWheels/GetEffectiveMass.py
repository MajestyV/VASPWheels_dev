import numpy as np
import matplotlib.pyplot as plt
from VaspWheels import Crystallography
from VaspWheels import GetEbands
from scipy.optimize import leastsq

GEB = GetEbands.Ebands()

class EffectiveMass:
    """ This class of function is designed to calculate effective mass and generate files needed for the calculation. """
    def __init__(self):
        self.name = EffectiveMass

    # 这个函数可以根据输入的倒格矢计算K空间中任意两点的距离，单位为Å^{-1}
    def Length(self, origin, destination, reciprocal_lattice):
        x, y, z = reciprocal_lattice                        # 倒格矢在正交直角坐标系上的表示，用于计算K空间中向量的长度
        input = [x, y, z, origin, destination]
        input_reform = [np.array(n) for n in input]         # 将所有输入数据从列表转换成数组
        x, y, z, origin, destination = input_reform         # 将转换后的数据从input_reform中解压出来
        K_vec = destination - origin                        # 计算由origin指向destination的K空间向量
        projected_K_vec = K_vec[0]*x+K_vec[1]*y+K_vec[2]*z  # 计算vec在正交直角坐标系下的坐标（投影）
        length = np.linalg.norm(projected_K_vec, ord=2)
        return length

    # 这个函数可以以某个点为起点（origin）往另一个点（destination）的方向进行坐标点插值
    # k_cutoff可以控制插值的范围，单位为Å^{-1}，比如：k_cutoff=0.015，则在距离origin 0.015Å远处取最后一个插值点
    # num_point可以控制生成插值点的个数
    def Interpolation(self,origin,destination,reciprocal_lattice=([1,0,0],[0,1,0],[0,0,1]),k_cutoff=0.015,num_point=6):
        x,y,z = reciprocal_lattice                                   # 倒格矢在正交直角坐标系上的表示，用于计算K空间中向量的长度
        input = [x,y,z,origin,destination]
        input_reform = [np.array(n) for n in input]                  # 将所有输入数据从列表转换成数组
        x,y,z,origin,destination = input_reform                      # 将转换后的数据从input_reform中解压出来
        vec = np.array(destination)-np.array(origin)                 # 计算起点指向终点的方向向量
        length = self.Length(origin,destination,reciprocal_lattice)  # 计算vec的长度
        destination_new = origin+vec*k_cutoff/length                 # 通过k_cutoff/length计算出插值的终点

        d_vec = (destination_new-origin)/(num_point-1)               # 通过插点数num_point计算出插点的间隔量d_vec
        point_list = []
        point = origin
        for i in range(num_point):
            point_list.append(point)
            point = point+d_vec                                      # 每跑一个循环增加一个d_vec向量

        return point_list

    # 这个函数可以用于生成计算有效质量所需的KPOINTS文件
    def GenKPOINTS(self,saving_directory, point_list):
        KPOINTS = saving_directory + 'KPOINTS'
        f = open(KPOINTS, 'w')
        f.write('auto generate\n' +                 # 写入表头文件
                str(len(point_list)) + '\n' +
                'Reciprocal\n')
        for i in range(len(point_list)):            # 根据point_list将K点一个个写入
            f.write(str(point_list[i][0]) + ' ' + str(point_list[i][1]) + ' ' + str(point_list[i][2]) + ' 1\n')
        f.close()
        return

    # 调用GetEbands中的函数提取EIGENVAL中的价带、导带数据及对应K点
    def GetBandEdge(self,EIGENVAL,VB_index,CB_index):
        Ebands_data = GEB.GetData(EIGENVAL)
        kpath = Ebands_data['kpath']
        energy = Ebands_data['energy']
        VB = energy[VB_index-1]    # VB-Valence Band, 价带
        CB = energy[CB_index-1]    # CB-Conduction Band, 导带
        return kpath, VB, CB

    # 通过scipy的最小二乘法拟合模块计算指定能带中的载流子有效质量
    # 根据Bloch theorem，1/m* = [d^2(E)/(dk)^2]/(h_bar)^2
    def CalEffectiveMass(self,k,E,guessing_para=(1,1,1)):
        input = [k, E, guessing_para]
        input_reform = [np.array(n) for n in input]  # 将所有输入数据从列表转换成数组
        k, E, guessing_para = input_reform           # 将转换后的数据从input_reform中解压出来

        # 应注意，V.A.S.P.中计算能带默认的长度单位是Å，能量单位是eV
        # 为了方便计算，并将最后的计算结果以电子静止质量m_{e}表示，我们需要将上述单位转换为原子单位制
        # 在原子单位制中，长度单位为Bohr， 1 Bohr = 0.529177210903 Å, 1 Bohr^{-1} = 1.8897261246257702 Å^{-1}
        # 能量单位为Hartree， 1 eV = 0.0367493 Hartree
        E_new = 0.0367493*E
        k_new = k/1.8897261246257702

        def function(p, x):
            A, B, C = p
            return A * x ** 2 + B * x + C

        def error(p, x, y):
            return function(p, x) - y

        para = leastsq(error, guessing_para, args=(k_new, E_new))

        m = 1/(2*para[0][0])  # 计算有效质量

        return m, para[0]

if __name__=='__main__':
    cryst = Crystallography.Crystal()
    EM = EffectiveMass()

    lattice = ['HEX', [3.1473295667554400, 3.1473295667554400, 43.9122903625234997, 90, 90, 120], 'primitive']
    crystal_class, lattice_para, cell_type = lattice
    reciprocal = cryst.Reciprocal_lattice(crystal_class,lattice_para)

    data_file = 'D:/Projects/PhaseTransistor/Data/Simulation/Conductivity/Mobility/4/EffectiveMass/4_GSE_EffectiveMass/'

    # This part is important
    part1 = EM.Interpolation([1/3.0, 1/3.0, 0],[0, 0, 0],reciprocal_lattice=reciprocal)
    part2 = EM.Interpolation([1/3.0, 1/3.0, 0],[2/3.0, 0, 0],reciprocal_lattice=reciprocal)
    part3 = EM.Interpolation([1/3.0, 1/3.0, 0],[0.500, 0, 0],reciprocal_lattice=reciprocal)
    part4 = EM.Interpolation([0.176666666667, 0.176666666667, 0],[0, 0, 0],reciprocal_lattice=reciprocal)
    part5 = EM.Interpolation([0.176666666667, 0.176666666667, 0],[1/3.0, 0, 0],reciprocal_lattice=reciprocal)
    part6 = EM.Interpolation([0, 0, 0],[1/3.0, 1/3.0, 0],reciprocal_lattice=reciprocal)
    total = part1+part2+part3+part4+part5+part6

    # EM.GenKPOINTS(data_file,total)

    EIGENVAL = data_file+'0.225/'+'EIGENVAL'
    k_point, vb,cb = EM.GetBandEdge(EIGENVAL,96,97)
    k = []
    vb_k = []   # 对应这段K点的价带
    cb_k = []   # 对应这段K点的导带
    for i in range(6):
        length = EM.Length(k_point[0],k_point[i],reciprocal)
        k.append(length)
        vb_k.append(np.array(vb[i]))
        cb_k.append(np.array(cb[i]))
    k = np.array(k)

    m, para = EM.CalEffectiveMass(k,vb_k)


    def function(p, x):
        A, B, C = p
        return A * x ** 2 + B * x + C

    x = np.linspace(0,0.008,100)

    plt.plot(k/1.8897261246257702,0.0367493*np.array(vb_k))
    plt.plot(x,function(para,x))

    print(para)
    print(m)