import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# In this code, non-resonance first-order Raman spectra is considered.

def GetDielectricConstant(file):
    # pandas.read_cvs函数可以通过header变量确定表头位置，header=0即将第一行作为表头
    data = pd.read_csv(file,sep="\s+",header=1)  # 以空格作为分隔符，\s匹配任意空白字符，等价于 [\t\n\r\f]
    title = data.columns  # 利用pandas的columns函数获取数据表头
    dimension = data.shape   # 利用pandas的shape函数获取数据的维度，格式为： （行数，列数）
    return data, title, dimension

# 根据V.A.S.P.计算结果构建光学介电常数矩阵
def DielectricTensor(epsilon11,epsilon22,epsilon33,epsilon12,epsilon23,epsilon13):
    input = [epsilon11,epsilon22,epsilon33,epsilon12,epsilon23,epsilon13]
    input_reform = [float(n) for n in input]  # 将所有输入数据转换成浮点数，以免出现整型使得最后计算结果出错
    epsilon11, epsilon22, epsilon33, epsilon12, epsilon23, epsilon13 = input_reform  # 将转换后的数据从input_reform中解压出来
    epsilon21 = epsilon12  # 光学介电常数张量应该是一个对称矩阵
    epsilon31 = epsilon13
    epsilon32 = epsilon23
    DT = np.mat([[epsilon11,epsilon12,epsilon13],
                 [epsilon21,epsilon22,epsilon23],
                 [epsilon31,epsilon32,epsilon33]])
    return DT

# 拉曼活性张量
def RamanActiveTensor(dielectric_tensor1,dielectric_tensor2,displacement,cell_volume):
    dielectric_tensor1 = np.mat(dielectric_tensor1)  # 将输入转换为np矩阵，防止数据类型错误
    dielectric_tensor2 = np.mat(dielectric_tensor2)
    differential_dielectric_tensor = dielectric_tensor1-dielectric_tensor2  # 差分介电常数张量=两个介电常数张量作矩阵差
    RAT = cell_volume*differential_dielectric_tensor/(4*np.pi*2*displacement)  # RAT - Raman Active Tensor
    return RAT

# 计算平均拉曼强度
def ScalarRamanIntensity(raman_active_tensor):
    I = raman_active_tensor
    term1 = 45*((I[0,0]+I[1,1]+I[2,2])/3.0)**2
    term2 = (7.0/2.0)*((I[0,0]-I[1,1])**2+(I[0,0]-I[2,2])**2+(I[1,1]-I[2,2])**2)
    term3 = (7.0/2.0)*6*(I[0,1]**2+I[0,2]**2+I[1,2]**2)
    I_scalar = term1+term2+term3  # 将公式拆成三部分，方便检查
    return I_scalar

# 利用phonon lifetime跟Heisenberg uncertainty principle计算damping项
def Damping(T):
    return 5

# 展宽函数
def NaturalBroadening(w,w_p,damping):
    w = np.array(w)  # 将输入转换为数组，防止数据类型错误
    gm = damping/2.0
    line_shape = gm/(np.pi*((w-w_p)**2+gm**2))
    return line_shape

def Raman(extent,peak,intensity,T=300,npoints=1000):
    origin, destination = extent  #解压终点跟起点
    w = np.linspace(origin,destination,npoints)  # w - wavenumber, 这个变量记录了计算拉曼光谱的波数范围
    damping = Damping(T)

    spectra = np.zeros(npoints)  # 创建一个一维的长度为npoints的全零数组
    for n in range(len(peak)):
        value = intensity[n]*NaturalBroadening(w,peak[n],damping)
        spectra = spectra+value

    return w, spectra  # 输出计算拉曼光谱的波数范围，以及对应的光谱

if __name__=='__main__':
    data_file = 'D:/Projects/PhaseTransistor/Data/Simulation/Raman/4/raman_0.100_LOPTICS_IPA/OUTCAR_Gallery/raman_0.100_IPA.dat'

    a = GetDielectricConstant(data_file)

    d, title, dim = a
    Mode = d['Mode'].values.T.tolist()  # 按列名从DataFrame数据中提取列数据，并转换成列表，以便操作
    # print(Mode)

    band = [4, 5, 6, 9, 10, 12, 15, 16, 19, 20, 21, 22, 25, 26, 30, 32, 34, 36]
    frequency = np.array([0.3178956434, 0.3179011422, 0.6122398479, 0.9791407984, 0.9791484453, 1.7441974870,
                          8.4270633389, 8.4270644076, 8.4980145329, 8.4980147666, 11.3823872417, 11.3823875524,
                          11.3938544631, 11.3938548430, 12.0769625411, 12.2598141670, 13.9745000930, 14.0311873921])
    omega = frequency*33.35641

    print(omega)

    X = d['X'].values.T.tolist()
    Y = d['Y'].values.T.tolist()
    Z = d['Z'].values.T.tolist()
    XY = d['XY'].values.T.tolist()
    YZ = d['YZ'].values.T.tolist()
    ZX = d['ZX'].values.T.tolist()

    I0 = []
    for i in band:
        n1 = Mode.index(i+0.001)
        n2 = Mode.index(i+0.002)
        x1, y1, z1, xy1, yz1, zx1 = [X[n1], Y[n1], Z[n1], XY[n1], YZ[n1], ZX[n1]]
        x2, y2, z2, xy2, yz2, zx2 = [X[n2], Y[n2], Z[n2], XY[n2], YZ[n2], ZX[n2]]

        dielec_tensor_1 = DielectricTensor(x1,y1,z1,xy1,yz1,zx1)
        dielec_tensor_2 = DielectricTensor(x2,y2,z2,xy2,yz2,zx2)

        raman_tensor = RamanActiveTensor(dielec_tensor_1,dielec_tensor_2,1,1)

        inten = ScalarRamanIntensity(raman_tensor)

        # print(inten)
        I0.append(inten)




    wavenumber, spectra_line = Raman([250,500],omega,I0)

    #et_1 = DielectricTensor(4,4,6,2,2,2)
    #et_2 = DielectricTensor(4,4,6,1.5,1.5,1.5)

    #raman_tensor = RamanActiveTensor(et_1,et_2,1,1)

    #i0 = ScalarRamanIntensity(raman_tensor)

    #print(raman_tensor)

    #print(i0)

    #plt.plot(x,NaturalBroadening(x,42,2))
    plt.plot(wavenumber,spectra_line)