# This code is written to extract electronic band structure data from V.A.S.P. calculation results.

import codecs
import re
import linecache  # 这个模块非常适合根据给出的行号， 从文本文件中读取指定行的数据
import numpy as np

class vasp:
    def __init__(self):
        self.name = vasp

    ##############################################################################################################
    # 一些通用函数

    # 这个函数利用linecache模块，可以从数据文件中读出指定行的信息，并以字符串形式返回
    # 应注意，这个函数的行数从1开始，即line_index=5指要读文件中的第五行
    def GrepLineContent(self,file,line_index):
        return linecache.getline(file,line_index).strip()

    # 此函数可将费米面调整为零，适用于energy为列表，一维数据，二维数组以及矩阵形式的数据的情况
    # 若输入的energy是一维数组或列表，对应于能量值是一维序列的情况，应用于调整态密度DOS的自变量
    # 若输入的energy是嵌套列表，二维数组或矩阵，对应于能量是二维能量面的情况，应用于调整能带图bands的高度
    def ShiftFermiSurface(self, energy, fermi_energy):
        energy_array = np.array(energy)  # 将输入转换为数组，确保下一步计算中的输入是数组（一维或二维）形式的数据
        return energy_array-fermi_energy

    ##############################################################################################################
    # 费米能级提取模块
    #

    ##############################################################################################################
    # 态密度（DOS）提取模块

    # This function is designed to read out DOS data from DOSCAR
    def ReadDOSCAR(self, DOSCAR):
        file = codecs.open(DOSCAR, 'rb', 'utf-8', 'ignore')  # Open file, using codecs to uniform coding type
        line = file.readline()
        lindex = 0  # line index
        data = []  # DOS数据
        while line:
            if lindex <= 4:
                pass  # The first five lines not terribly useful
            else:
                value = line.split()  # 以空字符（空格，换行'\n'，制表符'\t'等）为分隔符对字符串做切片 （什么都不填默认为空字符）
                value = list(map(float, value))
                data.append(value)

            line = file.readline()
            lindex += 1
        file.close()

        npoints = int(data[0][2])  # number of gridpoints on which the DOS is evaluated

        separated_data = []  # 分隔后的数据总集
        nrows = npoints + 1  # number of line in one data subset (一个数据子集的行数)
        nsubset = int(len(data) / nrows)  # number of data subsets (数据子集的个数)
        for i in range(nsubset):
            data_subset = []  # 数据子集，每次循环开始重新定义成空列表
            for j in range(nrows):
                data_subset.append(data[i * nrows + j])  # i标定了数据子集的序号，j标定了在这个子集中数据行的序号
            separated_data.append(data_subset)  # 将子集补充到分隔后的数据总集当中

        return separated_data

    # 利用ReadDOSCAR函数整理出态密度(DOS)
    def GetData(self, DOSCAR, spin_polarized='False'):
        data = self.ReadDOSCAR(DOSCAR)[0]  # 非投影的态密度在第一个子集当中
        npoints = int(data[0][2])  # number of gridpoints on which the DOS is evaluated
        Efermi = float(data[0][3])  # The Fermi energy

        if spin_polarized == 'False':
            key = ['energy', 'DOS', 'integrated DOS']
        else:
            key = ['energy', 'DOS-spin up', 'DOS-spin down', 'integrated DOS-spin up', 'intergrated DOS-spin down']
        DOS = dict.fromkeys(key)  # 根据列表key中的键生成DOS字典，对应键值为None
        for n in key:
            DOS[n] = []  # 将所以列表key中对于的键值改为空列表，用于存放数据
        DOS.update({'number': npoints, 'Efermi': Efermi})  # 将计算的能量点的个数跟费米能更新到DOS字典当中

        for i in range(len(data)):
            if i == 0:  # The first line is parameters (第一行都是参数)
                pass
            else:
                for j in key:
                    DOS[j].append(data[i][key.index(j)])  # key.index(j) - 利用j在列表key中的位置来分配对应数据到字典DOS中

        return DOS

    # 利用ReadDOSCAR函数整理出投影态密度(projected DOS)
    def GetProjectedData(self, DOSCAR, **kwargs):
        data_total = self.ReadDOSCAR(DOSCAR)
        natom = len(data_total) - 1  # 各个原子的态密度会分得一个子集，总DOS会分得一个子集，所以子集总数减1即为原子总数

        spin = kwargs['spin_polarized'] if 'spin_polarized' in kwargs else 'False'
        lm_decomposed = kwargs['lm_decomposed'] if 'lm_decomposed' in kwargs else 'False'
        # decomposition of azimuthal quantum number (角量子数) l and magnetic quantum number (磁量子数) m

        if spin == 'False':
            if lm_decomposed == 'False':
                key = ['energy', 's', 'p', 'd']  # s, p, d indicate the atomic orbital
            else:
                key = ['energy', 's', 'p_{y}', 'p_{z}', 'p_{x}', 'd_{xy}', 'd_{yz}', 'd_{z^2}', 'd_{xz}',
                           'd_{x^2-y^2}']
        else:
            key = ['energy', 's-spin up', 's-spin down', 'p-spin up', 'p-spin down', 'd-spin up', 'd-spin down']

        atom_list = kwargs['atom_list'] if 'atom_list' in kwargs else ['atom'+str(n+1) for n in range(natom)]
        # 如无指定，则根据原子个数生成原子名称

        DOS_projected = dict.fromkeys(atom_list)  # 根据atom_list创建一个字典，每个atom对应得键值都是一个空字典
        for i in atom_list:
            DOS_projected[i] = dict.fromkeys(key)
            for j in key:
                DOS_projected[i][j] = []  # 将对应原子中的对应键的值改为空列表，用于存放数据

        nrow_subset = len(data_total[0])  # 一个数据子集的行数
        for i in atom_list:
            subset_index = atom_list.index(i) + 1  # 由于总数据的第一个子集是总态密度，所以atom_list.index(i)要加1，即从第二个子集读起
            data_subset = data_total[subset_index]
            for j in range(nrow_subset):  # j标示着读这个数据子集的具体行数
                if j == 0:  # The first line is parameters (第一行都是参数)
                    pass
                else:
                    for k in key:
                        key_index = key.index(k)  # key.index(k) - 利用k在列表key中的位置来分配对应数据到字典中的具体位置
                        DOS_projected[i][k].append(data_subset[j][key_index])

        return DOS_projected

    ##############################################################################################################
    # 能带提取模块
    # This function is designed to extract electronic bands data from file EIGENVAL.
    def GetEbands(self,EIGENVAL):
        pattern_int = re.compile(r'-?\d+')  # 匹配整数，用于提取参数
        # pattern_float = re.compile(r'-?\d+\.\d+?[Ee]?-?\d+')  # 匹配可能有科学计数法的浮点数的正则表达式, 用于提取数据

        # 提取能带计算时的一些全局参数
        parameter_string = self.GrepLineContent(EIGENVAL,6)
        parameter = pattern_int.findall(parameter_string)  # 利用正则表达式提取出这一行所有的整数
        num_valence_electrons, num_kpoints, num_bands = parameter
        # 这行第一个数为价电子总数，第二个为k点路径总点数，第三个为能带总数
        num_valence_electrons = int(num_valence_electrons)  # 从文件中读取完的数据形式为字符串，需要转换为整型才能进行后续处理
        num_kpoints = int(num_kpoints)
        num_bands = int(num_bands)

        # 通过循环读取EIGENVAL中的数据
        file = codecs.open(EIGENVAL,'rb','utf-8','ignore')  # Open file, using codecs to uniform coding type
        line = file.readline()
        line_index = 1  # 读取文件时，为了方便，我们设定从一开始，那么line_index=1指文件的第一行
        raw_data = []   # 存放原始数据的列表
        while line:
            if line_index >= 7:  # 为了方便后续的编程跟数据处理，我们从EIGENVAL的第7行开始读
                value = line.split()  # 以空字符（空格，换行'\n'，制表符'\t'等）为分隔符对字符串做切片 （什么都不填默认为空字符）
                value = list(map(float,value))
                raw_data.append(value)

            line = file.readline()
            line_index += 1
        file.close()

        bands = np.zeros((num_bands,num_kpoints))        # 定义一个num_bands行num_kpoints列的矩阵用于存放能带数据
        occupation = np.zeros((num_bands, num_kpoints))  # 同理，定义一个矩阵存放电子占据数据，此矩阵跟能带矩阵具有相同的维度

        # 在EIGENVAL中，数据会按照K点路径顺序排布，每个K点的能带数据可以看作一个循环，那么我们便可以通过不断loop循环来将数据进行分类整理
        nrows_cycle = num_bands+2   # 每个循环的数据行数为：能带数+K点坐标行+空白分割行 = 能带数+2行
        Kpath, Kweight = [[],[]]  # 批量定义空列表准备储存数据，k_path是K点路径，k_weight是K点对应的权重
        for i in range(num_kpoints):
            # 确定各个数据对应的列表引索
            Kindex, band_data_starting = [i*nrows_cycle+1, i*nrows_cycle+2]
            Kpath.append([raw_data[Kindex][0],raw_data[Kindex][1],raw_data[Kindex][2]])  # K点路径
            Kweight.append(raw_data[Kindex][3])
            # 通过循环将能带数据赋值到刚刚创建的矩阵中
            for j in range(num_bands):
                bands[j,i] = raw_data[band_data_starting+j][1]
                occupation[j,i] = raw_data[band_data_starting+j][2]

        data_dict = {'num_kpoints': num_kpoints,          # K点路径上的取点数
                     'num_bands': num_bands,              # 能带数目
                     'Kpath': Kpath,                    # K点路径
                     'Kweight': Kweight,                # 每个K点对应的权重
                     'bands': np.array(bands),            # 能带数据（最后的输出为二维数组的话，操作空间会更大）
                     'occupation': np.array(occupation)}  # 轨道（能带）占据情况}

        return data_dict

    ###############################################################################################################
    # 能带分析模块
    # 这个模块的功能包括但不限于从静态自洽计算（SCF）结果中获取费米能级，或者通过能带占据情况确定费米能级位置
    # 以及计算禁带宽度，判断其为直接还是间接带隙等等

    # 若使用MajestyV的脚本计算电子能带，SCF计算结果中通常会生成一个总结文件Markdown_SCF，其中记载着准确的费米能级（没有分数占据的情况下）
    # MajestyV的github：https://github.com/MajestyV
    # 此函数可以从Markdown文件中提取费米能级的计算结果
    def GetFermiEnergy(self, Markdown_SCF):
        pattern = re.compile(r'-?\d+\.?\d+')  # 匹配浮点数的正则表达式
        file = codecs.open(Markdown_SCF, 'rb', 'utf-8', 'ignore')
        line = file.readline()
        energy = pattern.findall(line)
        Efermi = float(energy[0])
        return Efermi

    # 此函数可通过能带占据情况区分导带跟价带，提取能带边缘（带边，band edges）
    # 由于DFT算法本身的原因，会出现分子轨道（能带）被分数电子占据的情况，所以我们使用OrderPrecision控制占据情况的精确度
    # 如OrderPrecision=2，则精确到小数点后两位
    def GetBandEdges(self, EIGENVAL, accuracy_order=0):
        data_dict = self.GetEbands(EIGENVAL)  # 利用GetEbands函数从EIGENVAL文件提取能带数据
        num_bands = data_dict['num_bands']  # 提取能带总数
        num_kpoints = data_dict['num_kpoints']  # 提取K点总数
        bands = data_dict['bands']  # 能带具体的能量值
        occupation = data_dict['occupation']  # 能带的占据情况

        Unoccupied = []  # 这个列表用于存放所有未被占据的能带数据
        Occupied = []  # 这个列表用于存放所有已被占据的能带数据
        for n in range(num_kpoints):
            energy_unoccupied = []
            energy_occupied = []
            for m in range(num_bands):
                    energy = bands[m,n]
                    filling_condition = occupation[m][n]  # 电子的填充情况
                    if round(filling_condition, accuracy_order) == 0:  # 通过判断能带的占据情况来确定能带在费米面之下还是费米面之上
                        energy_unoccupied.append(energy)
                    else:
                        energy_occupied.append(energy)
            Unoccupied.append(energy_unoccupied)
            Occupied.append(energy_occupied)

        ConductionBand = [min(Unoccupied[i]) for i in range(len(Unoccupied))]  # 最低未占据能带（导带），Lowest unoccupied band
        ValenceBand = [max(Occupied[i]) for i in range(len(Occupied))]  # 最高已占据能带（价带），Highest occupied band

        return ValenceBand, ConductionBand

        # 此函数通过费米能级的位置区分导带跟价带（不太准确）
        def AnalyzeEfermi(self, EIGENVAL, Efermi=0):
            Bands = GE.GetData(EIGENVAL)  # 利用GetEbands模块从EIGENVAL文件提取能带数据
            energy = Bands['energy']  # 获取能带数据
            K_path = Bands['kpath']  # 获取计算EIGENVAL时的K空间路径
            occupation = Bands['occupation']  # 获取能带占据信息

            Unoccupied = []  # 这个列表用于存放所有未被占据的能带数据
            Occupied = []  # 这个列表用于存放所有已被占据的能带数据
            for n in range(len(K_path)):
                E_unoccupied = []
                E_occupied = []
                for m in range(len(energy)):
                    E = energy[m][n]
                    if E >= Efermi:  # 通过能量E是否大于给定的费米能级判断能带在费米面之下还是费米面之上
                        E_unoccupied.append(E)
                    else:
                        E_occupied.append(E)
                Unoccupied.append(E_unoccupied)
                Occupied.append(E_occupied)

            ConductionBand = [min(Unoccupied[i]) for i in range(len(Unoccupied))]  # 最低未占据能带（导带），Lowest unoccupied band
            ValenceBand = [max(Occupied[i]) for i in range(len(Occupied))]  # 最高已占据能带（价带），Highest occupied band

            return ValenceBand, ConductionBand

        # 此函数可以计算带隙（Bandgap），同时得出材料是直接带隙还是间接带隙
        def AnalyzeBandgap(self, EIGENVAL, **kwargs):
            mode = kwargs['mode'] if 'mode' in kwargs else 'Occupation'  # 默认通过电子占据情况分析带隙
            Precision = kwargs['Precision'] if 'Precision' in kwargs else 0  # 分析电子占据情况时所用的精确度
            Efermi = kwargs['Efermi'] if 'Efermi' in kwargs else 0.0  # 通常不使用此模式，故设Efermi为0

            if mode == 'Occupation':
                ValenceBand, ConductionBand = self.AnalyzeOccupation(EIGENVAL, Precision=Precision)
            elif mode == 'Efermi':
                ValenceBand, ConductionBand = self.AnalyzeEfermi(EIGENVAL, Efermi=Efermi)
            else:
                print(r'ERROR: The mode of this function could only be "Occupation" or "Efermi".')
                return

            Ev_max = max(ValenceBand)  # 价带顶
            Ec_min = min(ConductionBand)  # 导带底
            Eg = Ec_min - Ev_max  # 带隙

            # 分析价带顶跟导带底的位置
            extremum_position = (ValenceBand.index(Ev_max), ConductionBand.index(Ec_min))

            return Eg, Ev_max, Ec_min, extremum_position


if __name__=='__main__':
    EIGENVAL = 'D:/MaterialsGallery/Testing/MoS2_pawlda/MoS2_2H/1/result/EIGENVAL'
    ebands = vasp()
    # Gamma-M-K-Gamma-A-L-H-A
    a = ebands.GetEbands(EIGENVAL)
    #print(len(a['energy'][0]))
    #print(len(a['occupation'][31]))
    print(a)

    #kpath.GetKpath(saving_directory,path,59)