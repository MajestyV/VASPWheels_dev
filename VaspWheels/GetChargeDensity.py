import numpy as np
import codecs
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from matplotlib.pyplot import MultipleLocator

class charge:
    """ This class of function is written for extracting charge density information from CHGCAR or CHGDIFF.vasp. """
    def __init__(self):
        self.name = charge

    # 这个函数可以提取CHGCAR或者CHGDIFF.vasp文件中的数据，以字典的形式返回
    def ExtractCharge(self,CHGCAR):
        file = codecs.open(CHGCAR, 'rb', 'utf-8', 'ignore')
        line = file.readline()
        data = []
        while line:
            value = line.split()
            data.append(value)
            line = file.readline()
        file.close()

        data_dict = dict.fromkeys(
            ['system', 'scale', 'lattice', 'coordinate', 'atom', 'num_atom', 'atomic position', 'mesh', 'charge'])

        data_dict['system'] = data[0]
        data_dict['scale'] = float(data[1][0])
        data_dict['lattice'] = [list(map(float, data[n])) for n in range(2, 5)]
        data_dict['coordinate'] = data[7]
        data_dict['atom'] = data[5]
        data_dict['num_atom'] = data[6]

        num_atom = 0
        for i in range(len(data[6])):
            num_atom = num_atom + int(data[6][i])  # 计算总原子数

        data_dict['atomic position'] = [data[n] for n in range(8, 8 + num_atom)]
        data_dict['mesh'] = list(map(int, data[9 + num_atom]))

        charge_data = [list(map(float, data[n])) for n in range(10 + num_atom, len(data))]
        charge_data_rescale = []
        for i in range(len(charge_data)):
            for j in range(len(charge_data[i])):
                charge_data_rescale.append(charge_data[i][j])
        data_dict['charge'] = charge_data_rescale

        return data_dict

    # 根据V.A.S.P.的赋值规律，我们可以生成一套引索列表，用以确定每一个数据所在mesh在实空间中的位置
    def Index(self,x, y, z):
        index_list = []
        # index_array=np.zeros((x,y,z))
        for k in range(1, z + 1):  # 最后历遍z的坐标
            for j in range(1, y + 1):  # 然后历遍y的坐标
                for i in range(1, x + 1):  # 首先历遍x的坐标
                    index_list.append([i, j, k])

        return index_list

    # 将引索列表与数据进行对应
    def Mapping(self,data, x, y, z):
        mapped_data = np.zeros((x, y, z))
        index_list = self.Index(x, y, z)
        for n in range(len(index_list)):
            i, j, k = index_list[n]
            mapped_data[i - 1, j - 1, k - 1] = data[n]  # python里的引索从0开始

        return mapped_data
    # 由于V.A.S.P.生成的数据是电荷数量（密度*原胞体积），所以我们可以计算原胞体积并将其转换回电荷密度
    def Volume(self,lattice_vector):
        a, b, c = lattice_vector
        a = np.array(a)
        b = np.array(b)
        c = np.array(c)
        V_cell = np.dot(a, np.cross(b, c))
        return V_cell

    # 此函数可以将ExtractCharge函数提取得到的原始数据展开成画图可用的二维数组型数据
    def Map_to_2D(self,Data_dict,dimension=(48*6,640)):
        volume = self.Volume(Data_dict['lattice'])  # 计算原胞体积

        length, width = dimension  # 解压画图区域的长和宽

        # 整理数据
        x, y, z = Data_dict['mesh']
        CharDiff = self.Mapping(Data_dict['charge'], x, y, z)
        CharDiff_2D = np.zeros((width, length))
        for i in range(length):
            for j in range(width):
                CharDiff_2D[j, i] = CharDiff[(47-i)%48, i%48, j]/volume

        return CharDiff_2D

if __name__=='__main__':
    GCD = Charge()

    # 一些用于文章级结果图的matplotlib参数，由于这些参数都是通用的，所以可以作为全局变量设置
    plt.rcParams['xtick.direction'] = 'in'  # 将x轴的刻度线方向设置向内
    plt.rcParams['ytick.direction'] = 'in'  # 将y轴的刻度线方向设置向内
    font_config = {'font.family':'Times New Roman'}  # font.family设定所有字体为Times New Roman
    plt.rcParams.update(font_config)  # 但是对于希腊字母(e.g. α, β, γ等)跟各种数学符号之类的不适用, Latex语法如$\Gamma$会被判断为None
    plt.rcParams['mathtext.default'] = 'regular'  # 可以通过这个选项修改所有希腊字母以及数学符号为Times New Roman

    CHGDIFF = 'D:/PhD_research/Data/Simulation/MoS2/GSE/4/test/CHGDIFF-0.050.vasp'

    data = GCD.ExtractCharge(CHGDIFF)

    v=GCD.Volume(data['lattice'])  # 计算原胞体积

    # 重整数据
    x_100,y_100,z_100 = data['mesh']
    CharDiff = GCD.Mapping(data['charge'],x_100,y_100,z_100)
    charge_2D = np.zeros((640,48*6))
    for i in range(48*6):
        for j in range(640):
            charge_2D[j,i] = CharDiff[(47-i)%48,i%48,j]/v  # 通过取余数的方式，将同一区域的图像复制6次

    fig = plt.figure(figsize=(9,4.5),dpi=100,frameon=False)

    x_major_locator = MultipleLocator(48.9176)
    y_major_locator = MultipleLocator(48.96)

    x_array = np.arange(0,320,48.9176)
    x_array_new = np.arange(0,3.207,0.5)
    y_array = np.array(list(np.arange(-195.84,-0.1,48.96))+list(np.arange(0,215,48.96)))
    y_array_new = np.array(list(np.arange(-2,-0.1,0.5))+list(np.arange(0,2.3,0.5)))

    # 以子图的形式画差分电荷密度的等高线图
    axes_1 = fig.add_axes([0.65,0.2,0.2,0.6])
    axes_1.set_title('$\epsilon$ = 3 V/nm')
    image_1 = axes_1.imshow(charge_2D,extent=[0,320,-215,215],cmap='seismic',vmin=-6e-4,vmax=6e-4)
    axes_1.xaxis.set_major_locator(x_major_locator)
    axes_1.yaxis.set_major_locator(y_major_locator)
    axes_1.set_xticks(x_array,x_array_new)
    axes_1.set_yticks(y_array,y_array_new)
    axes_1.set_xlabel(r'($\vec{a}$-$\vec{b}$)-direction (nm)')
    axes_1.set_ylabel(r'$\vec{c}$-direction (nm)')

    # Colorbar
    axes_2 = fig.add_axes([0.90,0.25,0.01,0.5])

    def fmt(x, pos):               # 此函数可以用于改变刻度
        return round(x*10000,2)

    fig.colorbar(image_1,cax=axes_2,orientation='vertical',format=ticker.FuncFormatter(fmt))

    axes_2.set_title(r'${\times}10^{-4}$ e/${\AA}^3$')  # matplotlib里面埃(Angstrom)的正确打法为: \AA
    # 由于'\t'是转义字符，所以如果我们要打乘号'\times'，就在字符串前面加r，不然电脑会先识别成转义字符