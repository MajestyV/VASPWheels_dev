# 此代码专门用于提取VASP可读的晶体结构文件POSCAR或者CONTCAR中的数据，或者根据指定构型生成POSCAR文件用于第一性原理计算

import codecs, linecache
import numpy as np

########################################################################################################################
# 一些后续可能会重复调用的通用函数，在一开头定义，方便后续代码的编写跟维护

# 这个函数利用linecache模块，可以从数据文件中读出指定行的信息，并以字符串形式返回
# 应注意，这个函数的行数从1开始，即line_index=5指要读文件中的第五行
def GrepLineContent(file,line_index): return linecache.getline(file,line_index).strip()

########################################################################################################################
# POSCAR文件的读取模块

# This function can extract the information of the lattice structure from the POSCAR (CONTCAR) file for V.A.S.P..
def GetStructure(POSCAR):
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

    structure = {'system': system,
                 'scale': scale,
                 'atom': atom_species,
                 'num_atom': num_atom,
                 'coordinate_system': coordinate,
                 'lattice_vector': lattice_vector,
                 'atomic_position': np.array(atomic_position)}  # 将原子坐标信息转换为数组，以防出错
    return structure

########################################################################################################################
# POSCAR文件的生成模块


# 这个函数可以将晶体信息组装成一个POSCAR文件
    def WritePOSCAR(self,saving_directory=default_directory+'POSCAR_new',lattice_vector=None,atomic_position=None,crystal_info=None):
        file = codecs.open(saving_directory,'w')  # 创建文件并给予写入权限
        file.write(crystal_info['system']+'\n'+
                   str(crystal_info['scale'])+'\n')  # 写入系统的名称以及晶胞的缩放尺度
        for i in range(len(lattice_vector)):  # 写入晶格向量
            file.write(str(lattice_vector[i][0])+'         '+str(lattice_vector[i][1])+'         '+str(lattice_vector[i][2])+'\n')

        num_species = len(atomic_position['atomic_species'])  # 原子种类的数目
        for i in range(num_species):  # 写入原子种类
            if i == (num_species-1):
                file.write(str(atomic_position['atomic_species'][i])+'\n')
            else:
                file.write(str(atomic_position['atomic_species'][i])+'    ')

        for i in range(num_species):  # 写入不同原子种类中原子的数目
            if i == (num_species-1):
                file.write(str(atomic_position['num_atom'][i])+'\n')
            else:
                file.write(str(atomic_position['num_atom'][i])+'    ')

        file.write(crystal_info['coordinate']+'\n')  # 写入坐标系统类别（分数坐标还是笛卡尔坐标）

        num_atom = len(atomic_position['atomic_coordinate'])  # 总原子数目
        atomic_coordinate=atomic_position['atomic_coordinate']
        for i in range(num_atom):
            file.write(str(atomic_coordinate[i][0])+'         '+str(atomic_coordinate[i][1])+'         '+str(atomic_coordinate[i][2])+'\n')

        file.close()

        return