import numpy as np
import codecs

class structure:
    """ This class of function is designed to analysis the lattice structure from the POSCAR file."""
    def __init__(self):
        self.name = structure

    # This function can extract the information of the lattice structure from the POSCAR file.
    def GetStructure(self,POSCAR):
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
    def LatticeParameter(self,lattice_vector):
        #lattice_vector = lattice_vector.tolist()     # 确保输入是个列表，可以解压
        a_vec, b_vec, c_vec = lattice_vector         # 解压a, b, c基矢
        a_vec = np.array(a_vec)                      # 将列表转换为数组，防止出错
        b_vec = np.array(b_vec)
        c_vec = np.array(c_vec)
        a = np.linalg.norm(np.array(a_vec),ord=2)    # 向量的二范数即向量的模
        b = np.linalg.norm(np.array(b_vec),ord=2)
        c = np.linalg.norm(np.array(c_vec),ord=2)
        alpha = np.arccos(np.dot(b_vec,c_vec)/(b*c))  # 利用 cos(<a,b>) = a·b/(|a|·|b|)计算向量夹角
        beta = np.arccos(np.dot(a_vec,c_vec)/(a*c))   # 在python中，向量点乘（内积）可以通过np.dot()函数实现
        gamma = np.arccos(np.dot(a_vec,b_vec)/(a*b))
        return a,b,c,alpha,beta,gamma

    # 用于计算不同晶体坐标下的原子间距
    def BondLength(self,Atom_1, Atom_2, lattice_vector):
        a1, a2, a3 = lattice_vector
        lattice = np.mat([a1,a2,a3])
        lattice_T = np.transpose(lattice)
        MetricTensor = np.dot(lattice,lattice_T)  # 应注意，这里要用向量/矩阵的点乘，不是叉乘，不要弄混

        d_vec = np.mat(Atom_1)-np.mat(Atom_2)
        d_sqaure = d_vec*MetricTensor*np.transpose(d_vec)  # 同时，这里也是点乘
        d_sqaure = np.array(d_sqaure)  # 将d_square从矩阵形式转变为数组形式

        return np.sqrt(d_sqaure[0][0])

if __name__=='__main__':
    pass
    #Sturc_info = GetStructure(relaxed_structure)
    #lp = Sturc_info['lattice_parameter']  # lp - lattice parameter
    #atom_pos = Sturc_info['atomic_position']
    #natom = Sturc_info['num_atom']

    #num_Mo = int(natom[0])
    #num_S = int(natom[1])
    #Mo_1 = np.mat(atom_pos[0])
    #Mo_2 = np.mat(atom_pos[1])
    #S_1 = np.mat(atom_pos[num_Mo])
    #S_2 = np.mat(atom_pos[num_Mo + 1])
    #S_3 = np.mat(atom_pos[num_Mo + 2])
    #S_4 = np.mat(atom_pos[num_Mo + 3])

    #a0 = distance([1.0, 0, 0], [0, 0, 0], lp)
    #b0 = distance([0, 1.0, 0], [0, 0, 0], lp)
    #c_over_2 = distance([0, 0, np.array(Mo_1)[0][2]], [0, 0, np.array(Mo_2)[0][2]], lp)
    #d_Mo1_S1 = distance(Mo_1, S_1, lp)
    #d_Mo1_S2 = distance(Mo_1, S_2, lp)
    #d_Mo1_S3 = distance(Mo_1, S_3, lp)
    #d_Mo1_S4 = distance(Mo_1, S_4, lp)
    #d_Mo2_S1 = distance(Mo_2, S_1, lp)
    #d_Mo2_S2 = distance(Mo_2, S_2, lp)
    #d_Mo2_S3 = distance(Mo_2, S_3, lp)
    #d_Mo2_S4 = distance(Mo_2, S_4, lp)

    #print(a, a0)
    #print(b, b0)
    #print(c_over_2)
    #print(d_Mo1_S1, d_Mo1_S2, d_Mo1_S3, d_Mo1_S4)
    #print(d_Mo2_S1, d_Mo2_S2, d_Mo2_S3, d_Mo2_S4)