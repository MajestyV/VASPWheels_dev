# This code is written for extracting electronic band structure data from V.A.S.P. results.

import codecs
import re

class vasp:
    def __init__(self):
        self.name = vasp

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
            data = self.ReadDOS(DOSCAR)[0]  # 非投影的态密度在第一个子集当中
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
            data_total = self.ReadDOS(DOSCAR)
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

            atom_list = kwargs['atom_list'] if 'atom_list' in kwargs else ['atom' + str(n + 1) for n in
                                                                           range(natom)]  # 如无指定，则根据原子个数生成原子名称

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
        int_pattern = re.compile(r'-?\d+')  # 匹配整数，用于提取参数
        # float_pattern = re.compile(r'-?\d+\.\d+?[Ee]?-?\d+')  # 匹配可能有科学计数法的浮点数的正则表达式, 用于提取数据

        file = codecs.open(EIGENVAL,'rb','utf-8','ignore')  # Open file, using codecs to uniform coding type
        line = file.readline()
        lindex = 0  # line index
        nkpoints = 0  # 预设能带参数
        nbands = 0
        data = []  # 能带数据
        while line:
            if lindex <= 4:
                pass
            elif lindex == 5:
                parameters = int_pattern.findall(line)  # 提取能带图的参数：k点数以及能带数, 以字符串形式返回
                parameters = list(map(int,parameters))  # 利用map函数对所有的字符串转化为浮点数，但是由于python3中map返回的是iterators类型， 所以还要用list函数将其转换回列表
                nkpoints = parameters[1]  # number of kpoints
                nbands = parameters[2]  # number of bands
            else:
                value = line.split()  # 以空字符（空格，换行'\n'，制表符'\t'等）为分隔符对字符串做切片 （什么都不填默认为空字符）
                value = list(map(float,value))
                data.append(value)

            line = file.readline()
            lindex += 1
        file.close()

        bands = {'number': nbands,
                 'energy': [[] for i in range(nbands)],  # 注意，此处不能有 [[]]*nbands，这样子做的话大列表中的子列表指针的内存会指向同一块
                 'occupation': [[] for i in range(nbands)],  # 关于上述问题，参考：https://zhuanlan.zhihu.com/p/88197389
                 'kpath': [],
                 'num kpoints': nkpoints}
        nrows = nbands+2  # number of line in one data subset (一个数据子集的行数)
        for i in range(len(data)):
            if i % nrows == 0:  # The first row are useless
                pass
            elif i % nrows == 1:  # The second row gives out the K-path
                bands['kpath'].append([data[i][0],data[i][1],data[i][2]])
            else:
                band_index = int(data[i][0]-1)  # 能带标识，在EIGENVAL里面，能带序号从1开始
                energy = data[i][1]  # 能量值
                occupation = data[i][2]  # 标示能带是否被占据
                bands['energy'][band_index].append(energy)
                bands['occupation'][band_index].append(occupation)

        return bands

    ###############################################################################################################
    # 费米面调零模块
    # 对应于能量值是连续一维的情况，应用于调整DOS的自变量（因此输入的energy应该是一维数组亦或是列表）
    def ShiftFermi_Energy(self, energy, fermi_energy):
        shifted_energy = []
        for i in range(len(energy)):
            shifted_energy.append(energy[i] - fermi_energy)
        return shifted_energy

    # 对应于能量是二维能量面的情况，应用于调整能带图bands的高度（因此输入的energy应该是嵌套的列表亦或是二维数组）
    def ShiftFermi(self,energy, fermi_energy):
        nbands = len(energy)  # number of bands
        nkpoints = len(energy[0])  # number of k points calculated
        shifted_energy = [[] for n in range(nbands)]
        for i in range(nbands):
            for j in range(nkpoints):
                shifted_energy[i].append(energy[i][j] - fermi_energy)
        return shifted_energy





if __name__=='__main__':
    EIGENVAL = 'D:/MaterialsGallery/Testing/MoS2_pawlda/MoS2_2H/1/result/EIGENVAL'
    ebands = vasp()
    # Gamma-M-K-Gamma-A-L-H-A
    a = ebands.GetEbands(EIGENVAL)
    #print(len(a['energy'][0]))
    #print(len(a['occupation'][31]))
    print(a)

    #kpath.GetKpath(saving_directory,path,59)