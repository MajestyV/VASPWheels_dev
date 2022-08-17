import codecs
import numpy as np

class LatteOpera:
    """ This class of function is ..."""
    def __init__(self):
        self.name = LatteOpera

    # 这个函数可以将晶体信息组装成一个POSCAR文件
    # 输入变量atomic_species的格式为[['atom1', num_atom1], ['atom2', num_atom2] ...]
    def WritePOSCAR(self,saving_directory,lattice_vector,atomic_species,atomic_position,**kwargs):
        file_name = kwargs['file_name'] if 'file_name' in kwargs else 'NewStructure.vasp'  # 文件名称，默认为VESTA可读的vasp文件
        scale = kwargs['scale'] if 'scale' in kwargs else 1.0  # 缩放因子，默认为1.0
        crystal_info = kwargs['crystal'] if 'crystal_info' in kwargs else 'New structure'  # 晶体名称
        coordinate = kwargs['coordinate'] if 'coordinate' in kwargs else 'Direct'  # 坐标系统，默认为Direct，即分数坐标

        target_file = saving_directory+'/'+file_name  # 目标结构文件的绝对地址

        file = codecs.open(target_file,'w')  # 创建文件并给予写入权限
        file.write(crystal_info+'\n'+  # 写入晶体名称
                   str(scale)+'\n')   # 写入晶胞的缩放因子
        for i in range(len(lattice_vector)):  # 写入晶格向量
            file.write(str(lattice_vector[i][0])+'         '+str(lattice_vector[i][1])+'         '+str(lattice_vector[i][2])+'\n')

        atomic_species = np.array(atomic_species)  # 将原子种类变量转换为二维数组，方便引用
        atom = atomic_species[:,0]   # 数组的第一列为原子种类
        natom = atomic_species[:,1]  # 数组的第二列为不同种类原子对应的原子数目
        for i in range(len(atom)):  # 写入原子种类
            if i == (len(atom)-1):
                file.write(atom[i]+'\n')
            else:
                file.write(atom[i]+'    ')
        for i in range(len(natom)):  # 写入不同原子种类中原子的数目
            if i == (len(natom)-1):
                file.write(str(natom[i])+'\n')
            else:
                file.write(str(natom[i])+'    ')

        file.write(coordinate+'\n')  # 写入坐标系统类别（分数坐标还是笛卡尔坐标）

        natom = [int(natom[n]) for n in range(len(natom))]  # 由于数组中有字符串，所以natom的元素被理解为字符串，要重新转换会整型
        natom_total = sum(natom)  # 总原子数目
        for i in range(natom_total):
            file.write(str(atomic_position[i][0])+'         '+str(atomic_position[i][1])+'         '+str(atomic_position[i][2])+'\n')

        file.close()

        return

    # 这个函数可以求出original_lattice坐标系中的坐标点fractional_coordinates，在新的坐标系target_lattice中的坐标
    # 可以用于坐标轴基矢变换
    # original_lattice跟target_lattice的输入可以是二维数组，列表亦或是numpy矩阵，基本格式为
    # [[a1, a2, a3], [b1, b2, b3], [c1, c2, c3]]
    # 其中，如a-axis的基矢[a1, a2, a3]则是由正交直角坐标系表示（Cartesian frame）
    def LatticeTransform(self,fractional_coordinates,original_lattice,target_lattice):
        coordinates_old = np.array(fractional_coordinates)  # 将原子分数坐标列表转换为二维数组
        g1 = np.mat(original_lattice)   # 确保晶格矩阵的格式为numpy矩阵
        g2 = np.mat(target_lattice)     # g1与g2的维度都应该是dim=(3x3)
        g2_inverse = np.linalg.inv(g2)

        coordinates_new = []
        for n in range(len(coordinates_old)):
            r = np.array([coordinates_old[n]])  # 将原子坐标转换成二维数组以便后续计算，dim=(1x3)
            r_projected = np.dot(r,g1)
            r_new = np.dot(r_projected,g2_inverse)  # rt = r·g1·g2^(-1)
            coordinates_new.append(np.array(r_new)[0])  # 将r_new转换为二维数组之后取第一行，mat变量无法进行此操作
            #print(np.array(r_new)[0])

        return np.array(coordinates_new)

    # 这个函数可以将晶体进行移动，不改变原胞形状
    def ShiftCrystal(self,atomic_position,shifting_vector):
        atomic_position = np.array(atomic_position)  # 将输入转换为数组
        Sv = np.array(shifting_vector)
        atomic_position_new = np.array([atomic_position[n]+Sv for n in range(len(atomic_position))]) # 将各个原子的位置进行移动
        return atomic_position_new

    # 结构近似
    def CutOff(self,atomic_position):
        for i in range(len(atomic_position)):
            for j in range(len(atomic_position[0])):
                atomic_position[i][j] = round(atomic_position[i][j],5)
        return atomic_position

    #atoms = np.array([['Mo', 1], ['S', 2]])

    #print(atoms[:,0])

if __name__=='__main__':
    lo = LatteOpera()
    file_dir = 'D:/Projects/PhaseTransistor/Data/Simulation/Phase/test'

    a = np.array([3.1900000572,0.0000000000,0.0000000000])
    b = np.array([-1.5950000286,2.7626210876,0.0000000000])
    # c = [0.0000000000,0.0000000000,12.2950000000]
    # s = np.array([0.0000000000, 0.0000000000, 3.79])
    s = np.array([0.0000000000,0.0000000000,24.59])
    Tv = np.array([0.0000000000,0.0000000000,20.0])

    lattice_old = [a,a+2*b,s]

    lattice_new = [a,a+2*b,s+Tv]

    #print(lattice_new)

    # 2H
    #pos = [[0.0,       0.0,       1.0/2.0],
           #[1.0/2.0,   1.0/2.0,   1.0/2.0],
           #[1.0/2.0,   1.0/6.0,   1.0    ],
           #[1.0/2.0,   1.0/6.0,   0.0    ],
           #[0.0,       2.0/3.0,   1.0    ],
           #[0.0,       2.0/3.0,   0.0    ]]

    # 2H_4 layer
    #pos = [[0.0,       0.0,       1.0/8.0],  # first layer
           #[1.0/2.0,   1.0/2.0,   1.0/8.0],
           #[1.0/2.0,   1.0/6.0,   0.20206],
           #[1.0/2.0,   1.0/6.0,   0.04794],
           #[0.0,       2.0/3.0,   0.20206],
           #[0.0,       2.0/3.0,   0.04794],
           #[1.0/2.0,   1.0/6.0,   3.0/8.0],  # second layer
           #[0.0,       2.0/3.0,   3.0/8.0],
           #[0.0,       0.0,       0.45206],
           #[0.0,       0.0,       0.29794],
           #[1.0/2.0,   1.0/2.0,   0.45206],
           #[1.0/2.0,   1.0/2.0,   0.29794],
           #[0.0,       0.0,       5.0/8.0],  # third layer
           #[1.0/2.0,   1.0/2.0,   5.0/8.0],
           #[1.0/2.0,   1.0/6.0,   0.70206],
           #[1.0/2.0,   1.0/6.0,   0.54794],
           #[0.0,       2.0/3.0,   0.70206],
           #[0.0,       2.0/3.0,   0.54794],
           #[1.0/2.0,   1.0/6.0,   7.0/8.0],  # fourth layer
           #[0.0,       2.0/3.0,   7.0/8.0],
           #[0.0,       0.0,       0.95206],
           #[0.0,       0.0,       0.79794],
           #[1.0/2.0,   1.0/2.0,   0.95206],
           #[1.0/2.0,   1.0/2.0,   0.79794]]

    # 2H_4 layer_rearranged
    pos = [[0.0, 0.0, 1.0 / 8.0],    # Mo
           [1.0 / 2.0, 1.0 / 2.0, 1.0 / 8.0],
           [1.0 / 2.0, 1.0 / 6.0, 3.0 / 8.0],
           [0.0, 2.0 / 3.0, 3.0 / 8.0],
           [0.0, 0.0, 5.0 / 8.0],
           [1.0 / 2.0, 1.0 / 2.0, 5.0 / 8.0],
           [1.0 / 2.0, 1.0 / 6.0, 7.0 / 8.0],
           [0.0, 2.0 / 3.0, 7.0 / 8.0],
           [1.0 / 2.0, 1.0 / 6.0, 0.18478],   # S
           [1.0 / 2.0, 1.0 / 6.0, 0.06522],
           [0.0, 2.0 / 3.0, 0.18478],
           [0.0, 2.0 / 3.0, 0.06522],
           [0.0, 0.0, 0.43478],
           [0.0, 0.0, 0.31522],
           [1.0 / 2.0, 1.0 / 2.0, 0.43478],
           [1.0 / 2.0, 1.0 / 2.0, 0.31522],
           [1.0 / 2.0, 1.0 / 6.0, 0.68478],
           [1.0 / 2.0, 1.0 / 6.0, 0.56522],
           [0.0, 2.0 / 3.0, 0.68478],
           [0.0, 2.0 / 3.0, 0.56522],
           [0.0, 0.0, 0.93478],
           [0.0, 0.0, 0.81522],
           [1.0 / 2.0, 1.0 / 2.0, 0.93478],
           [1.0 / 2.0, 1.0 / 2.0, 0.81522]]

    # 1T
    #pos = [[0.0,       0.0,       1.0/2.0],
           #[1.0/2.0,   1.0/2.0,   1.0/2.0],
           #[1.0/2.0,   1.0/6.0,   1.0    ],
           #[0.0,       1.0/3.0,   0.0    ],
           #[0.0,       2.0/3.0,   1.0    ],
           #[1.0/2.0,   5.0/6.0,   0.0    ]]

    # 1T_prime
    #pos = [[0.0,       0.0,      0.5    ],
           #[0.5,       0.3986,   0.5    ],
           #[0.5,       0.1407,   1.0    ],
           #[0.0,       0.3005,   0.0    ],
           #[0.0,       0.6487,   0.8514 ],
           #[0.5,       0.7922,   0.1486 ]]

    pos_new = lo.LatticeTransform(pos,lattice_old,lattice_new)

    pos_shifted = lo.ShiftCrystal(pos_new,[0.0,0.0,10.0/(20+24.59)])

    print(pos_shifted)

    pos_shifted_rounded = lo.CutOff(pos_shifted)

    lo.WritePOSCAR(file_dir,lattice_new,[['Mo',8],['S',16]],pos_shifted_rounded)