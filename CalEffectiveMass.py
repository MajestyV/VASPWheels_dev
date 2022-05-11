import numpy as np
import matplotlib.pyplot as plt
from VaspWheels import Crystallography
from VaspWheels import GetEbands
from scipy.optimize import leastsq

cryst = Crystallography.Crystal()
GEB = GetEbands.Ebands()

lattice = ['HEX', [3.1473295667554400, 3.1473295667554400, 43.9122903625234997, 90, 90, 120], 'primitive']
reciprocal = cryst.Reciprocal_lattice('HEX',[3.1473295667554400, 3.1473295667554400, 43.9122903625234997, 90, 90, 120])

data_file = 'D:/Projects/PhaseTransistor/Data/Simulation/Conductivity/Mobility/4/EffectiveMass/4_GSE_EffectiveMass/'

# a1, a2, a3 = [3.1473295667554400, 3.1473295667554400, 43.9122903625234997]

def Interpolation(Starting_point,Stopping_point,frame=([1,0,0],[0,1,0],[0,0,1]),k_cutoff=0.015,num_point=6):
    x,y,z = frame
    input = [x,y,z,Starting_point,Stopping_point]
    input_reform = [np.array(n) for n in input]              # 将所有输入数据从列表转换成数组
    x,y,z,Starting_point,Stopping_point = input_reform       # 将转换后的数据从input_reform中解压出来
    vec = np.array(Stopping_point)-np.array(Starting_point)  # 计算起点指向终点的方向向量
    projected_vec = vec[0]*x+vec[1]*y+vec[2]*z               # 计算vec在正交直角坐标系下的坐标（投影）
    length = np.linalg.norm(projected_vec,ord=2)             # 计算vec的长度
    Stopping_point_new = Starting_point+vec*k_cutoff/length  # 通过k_cutoff/length计算出插值的终点

    d_vec = (Stopping_point_new-Starting_point)/(num_point-1)  # 通过插点数num_point计算出插点的间隔量d_vec
    point_list = []
    point = Starting_point
    for i in range(num_point):
        point_list.append(point)
        point = point+d_vec                                    # 每跑一个循环增加一个d_vec向量

    return point_list

def ProjectK(K_point,origin,frame):
    x, y, z = frame
    input = [x, y, z, K_point, origin]
    input_reform = [np.array(n) for n in input]  # 将所有输入数据从列表转换成数组
    x, y, z, K_point, origin = input_reform  # 将转换后的数据从input_reform中解压出来
    K_point = K_point-origin
    projected_K = K_point[0] * x + K_point[1] * y + K_point[2] * z  # 计算vec在正交直角坐标系下的坐标（投影）
    length = np.linalg.norm(projected_K, ord=2)
    return length

def GenKPOINTS(saving_directory,point_list):
    KPOINTS = saving_directory+'KPOINTS'
    f = open(KPOINTS,'w')
    f.write('auto generate\n'+
            str(len(point_list))+'\n'+
            'Reciprocal\n')
    for i in range(len(point_list)):
        f.write(str(point_list[i][0])+' '+str(point_list[i][1])+' '+str(point_list[i][2])+' 1\n')
    f.close()
    return

def GetBandEdge(VB_index,CB_index,data):
    VB = data[VB_index-1]
    CB = data[CB_index-1]
    return VB,CB

# 用于计算有效质量的模块
p0 = [1,1,1]  # 初猜

def function(p,x):
    A,B,C = p
    return A*x**2+B*x+C

def error(p,x,y):
    return function(p,x)-y


# This part is important
part1 = Interpolation([1/3.0, 1/3.0, 0],[0, 0, 0],frame=reciprocal)
part2 = Interpolation([1/3.0, 1/3.0, 0],[2/3.0, 0, 0],frame=reciprocal)
part3 = Interpolation([1/3.0, 1/3.0, 0],[0.500, 0, 0],frame=reciprocal)
part4 = Interpolation([0.176666666667, 0.176666666667, 0],[0, 0, 0],frame=reciprocal)
part5 = Interpolation([0.176666666667, 0.176666666667, 0],[1/3.0, 0, 0],frame=reciprocal)
part6 = Interpolation([0, 0, 0],[1/3.0, 1/3.0, 0],frame=reciprocal)
total = part1+part2+part3+part4+part5+part6

# GenKPOINTS(data_file,total)

#print(ProjectK([0.176666666667, 0.176666666667, 0],[1/3,1/3,0],reciprocal))

Ebands_data = GEB.GetData(data_file+'0.025/'+'EIGENVAL')

kpath = Ebands_data['kpath']
energy =  Ebands_data['energy']

#print(len(energy[0]))

vb,cb = GetBandEdge(96,97,energy)
K = []
vb_k = []   # 对应这段K点的价带
cb_k = []   # 对应这段K点的导带
for i in range(6):
    proj_K = ProjectK(kpath[i],kpath[0],reciprocal)
    K.append(proj_K)
    vb_k.append(vb[i])
    cb_k.append(cb[i])
K = np.array(K)
vb_k = np.array(vb_k)


p0 = np.array([1.0,1.0,1.0])
para = leastsq(error,p0,args=(K,vb_k))

x0 = np.linspace(0,0.015,100)
plt.plot(K,vb_k)
plt.plot(x0,function(para[0],x0))

print(para)



#test = np.linspace(0,36,36)
#plt.plot(test,vb)
#plt.ylim(1.42,1.44)