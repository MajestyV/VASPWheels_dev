# 此代码囊括了一系列的函数，以实现一系列功能，致力于为第一性原理研究中常见的数据分析与计算提供便利
# 高聚低耦，吾码所宗，以建理论，追本溯源

import codecs
import numpy as np
import pandas as pd
from scipy.optimize import leastsq

class functions:
    """ This class of functions is designed for general data analysis and computation in ab initio study. """
    def __init__(self):
        self.name = functions

    ##############################################################################################################
    # 通用数据提取以及保存模块
    # 此函数可以利用pandas提取文件中的数据，适用于txt、dat、csv等格式的文件
    # 数据文件中的数据形式应为两列式，如：第一列为自变量，第二列为因变量
    def GetData(self, data_file, **kwargs):
        header = kwargs['header'] if 'header' in kwargs else None  # 文件中的数据列，默认为没有列名，第一行作为数据读取
        sep = kwargs['sep'] if 'sep' in kwargs else '\s+'  # 数据分隔符，默认为'\s+'（指代\f\n\t\r\v这些）
        # 利用pandas提取数据，得到的结果为DataFrame格式
        data_DataFrame = pd.read_csv(data_file, header=header, sep=sep)  # 若header=None的话，则设置为没有列名
        data_array = data_DataFrame.values  # 将DataFrame格式的数据转换为数组

        x_col = kwargs['x_col'] if 'x_col' in kwargs else 0  # 默认第一列为自变量所在列
        y_col = kwargs['y_col'] if 'y_col' in kwargs else 1  # 默认第二列为因变量所在列
        x = data_array[:, x_col]  # 默认第一列为自变量
        y = data_array[:, y_col]  # 默认第二列为因变量
        return x, y

    # 此函数可以利用pandas包记录数据，应注意输入的数据应为二维数组或是二维列表
    def SaveData(self, saving_directory, data, **kwargs):
        file_name = kwargs['file_name'] if 'file_name' in kwargs else 'Untitled'  # 文件名，默认为Untitled
        format = kwargs['format'] if 'format' in kwargs else 'csv'  # 保存文件格式，默认为csv
        saving_address = saving_directory + file_name + '.' + format

        data = np.array(data)  # 确保输入数据为二维数组
        shape = data.shape  # 获取data的维数
        row_index = kwargs['row_index'] if 'row_index' in kwargs else [i + 1 for i in range(shape[0])]  # 行引索
        col_index = kwargs['col_index'] if 'col_index' in kwargs else [i + 1 for i in range(shape[1])]  # 列引索
        data_df = pd.DataFrame(data, index=row_index, columns=col_index)  # 将数据转换为pandas专用的DataFrame格式

        sep = kwargs['sep'] if 'sep' in kwargs else ','  # 数据分隔符，默认为','
        data_df.to_csv(saving_address, index=True, header=True, sep=sep)  # 保存数据

        ### 在csv文件中第一行添加分隔符信息，这样子excel读取csv文件的时候才不会排版错乱
        with open(saving_address, 'r+', encoding='utf-8') as file:
            content = file.read()  # 将已有的内容读取出来
            file.seek(0, 0)  # 找到数据文件的开头
            file.write('sep=' + sep + '\n' + content)  # 写入分隔符信息
        return

    ##############################################################################################################
    # 常用的运算或是拟合函数

    #coef_list = []
    #EM_list = []
    #for i in range(num_segment):
        #coef = np.polyfit(Kpath_segment, band_segmented[i], 2)  # 利用polyfit对能带进行二次项拟合
        #coef_list.append(coef)
        #m_effective = 1 / (2 * coef[0])
        #EM_list.append(m_effective)


    ##############################################################################################################
    #########################################接下来的部分为特定功能的实现模块###########################################
    ##############################################################################################################
    # V.A.S.P.计算中的结构文件POSCAR的分析模块
    # This function can extract the information of the lattice structure from the POSCAR file.
    def GetStructure(self, POSCAR):
        file = codecs.open(POSCAR, 'rb', 'utf-8', 'ignore')
        line = file.readline()
        lindex = 0
        lattice_vector = []
        atomic_position_raw = []
        while line:
            content = line.split()  # 以空字符（空格，换行'\n'，制表符'\t'等）为分隔符对本行内容做切片 （什么都不填默认为空字符）
            if lindex == 0:
                system = line.split()
            elif lindex == 1:
                scale = float(content[0])
            elif lindex >= 2 and lindex <= 4:
                content = list(map(float, content))
                lattice_vector.append(content)
            elif lindex == 5:
                atom_species = content
            elif lindex == 6:
                num_atom = list(map(float, content))
            elif lindex == 7:
                coordinate = content[0]
            else:
                content = list(map(float, content))
                atomic_position_raw.append(content)

            line = file.readline()
            lindex += 1
        file.close()

        # 重整原子坐标信息，丢弃无意义的部分
        num_total = int(sum(num_atom))  # 将各原子数加起来得到原子总数,记得要替换为整型
        atomic_position = []
        for i in range(num_total):
            atomic_position.append(atomic_position_raw[i])

        structure = {'system': system, 'scale': scale,
                     'atom': atom_species, 'num_atom': num_atom,
                     'coordinate_system': coordinate,
                     'lattice_vector': lattice_vector,
                     'atomic_position': np.array(atomic_position)}  # 将原子坐标信息转换为数组，以防出错
        return structure

    # 这个函数可以通过晶体的三个基矢a, b, c计算晶格常数，但是记得输入必须是个由三个基矢组成的列表：[[a],[b],[c]]，方便解压
    def LatticeParameter(self, lattice_vector):
        # lattice_vector = lattice_vector.tolist()     # 确保输入是个列表，可以解压
        a_vec, b_vec, c_vec = lattice_vector  # 解压a, b, c基矢
        a_vec = np.array(a_vec)  # 将列表转换为数组，防止出错
        b_vec = np.array(b_vec)
        c_vec = np.array(c_vec)
        a = np.linalg.norm(np.array(a_vec), ord=2)  # 向量的二范数即向量的模
        b = np.linalg.norm(np.array(b_vec), ord=2)
        c = np.linalg.norm(np.array(c_vec), ord=2)
        alpha = np.arccos(np.dot(b_vec, c_vec) / (b * c))  # 利用 cos(<a,b>) = a·b/(|a|·|b|)计算向量夹角
        beta = np.arccos(np.dot(a_vec, c_vec) / (a * c))  # 在python中，向量点乘（内积）可以通过np.dot()函数实现
        gamma = np.arccos(np.dot(a_vec, b_vec) / (a * b))
        return a, b, c, alpha, beta, gamma

    # 用于计算不同晶体坐标下的原子间距
    def BondLength(self, Atom_1, Atom_2, lattice_vector):
        a1, a2, a3 = lattice_vector
        lattice = np.mat([a1, a2, a3])
        lattice_T = np.transpose(lattice)
        MetricTensor = np.dot(lattice, lattice_T)  # 应注意，这里要用向量/矩阵的点乘，不是叉乘，不要弄混

        d_vec = np.mat(Atom_1) - np.mat(Atom_2)
        d_sqaure = d_vec * MetricTensor * np.transpose(d_vec)  # 同时，这里也是点乘
        d_sqaure = np.array(d_sqaure)  # 将d_square从矩阵形式转变为数组形式

        return np.sqrt(d_sqaure[0][0])

    ##############################################################################################################
    # Carrier transportation calculation module (载流子输运计算模块)

    # 能带载流子有效质量计算，详见：N. W. Ashcroft, N. D. Mermin. Soild State Physics, ISBN-13: 978-0030839931.
    # 以及面向维基科研：https://en.wikipedia.org/wiki/Effective_mass_(solid-state_physics)
    # 此函数可以计算在能带中运动的载流子的有效质量
    def CalculateEffectiveMass(self,Kstep,band,num_segment,**kwargs):
        num_point_total = len(band)  # 能带总点数
        num_point_segment = int(len(band)/num_segment)  # 每段能带中包含的点数
        # 每一段能带中，用于计算有效质量的点数，如不设置，则默认每段能带所有点都用于计算有效质量
        num_point_evaluating = kwargs['points_evaluating'] if 'points_evaluating' in kwargs else num_point_segment

        # 应注意，V.A.S.P.中计算能带默认的长度单位是Å，能量单位是eV，为将最后结果以电子静止质量m_{e}表示，我们需将输入数据转换为原子单位制
        # 在原子单位制中，长度单位为Bohr， 1 Bohr = 0.529177210903 Å, 1 Bohr^{-1} = 1.8897261246257702 Å^{-1}
        # 能量单位为Hartree， 1 eV = 0.0367493 Hartree
        Kstep = Kstep/1.8897261246257702  # K点路程中，每个点直接间隔的距离
        band = 0.0367493*np.array(band)

        Kpath_segment = np.array([i*Kstep for i in range(num_point_evaluating)])  # 生成衡量有效质量的能带的K空间路程点
        band_segmented = [band[i:i+num_point_evaluating] for i in range(0,num_point_total,num_point_segment)]  # 能带分段

        # 接下来我们对运动在能带上的载流子的有效质量进行计算（https://yh-phys.github.io/2019/10/26/vasp-2d-mobility/）
        # 考虑到有效质量实际上就是能带曲率的倒数，我们先利用scipy的最小二乘法模块对能带进行二次项拟合，再对二次项的系数进行计算即可
        # 要利用scipy进行拟合，我们首先要定义两个函数
        # 由于我们的K点路径段平移到了原点开始，所以我们只需要考虑形如y=a*x^2+c的二次多项式，不需要考虑一次项（多项式关于y轴对称，没有平移项）
        def polynomial(coefficient,x): return coefficient[0]*x**2+coefficient[1]
        def error(coefficient,x,y): return polynomial(coefficient,x)-y  # 拟合误差

        # scipy的最小二乘法拟合模块需要一个初猜值
        initial_guess = kwargs['initial_guess'] if 'initial_guess' in kwargs else np.array([1, 1])
        EffectiveMass_list = []
        for i in range(num_segment):
            coef = leastsq(error, initial_guess, args=(Kpath_segment, band_segmented[i]))
            m_eff = 1.0/(2*coef[0][0])  # 计算有效质量
            EffectiveMass_list.append(m_eff)

        return EffectiveMass_list


    ##############################################################################################################
    # 弹性模量计算模块（应变-能量分析）

    ##############################################################################################################
    # 未知领域