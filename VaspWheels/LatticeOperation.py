# This code is written for conducting various of lattice manipulations like forming supercell, exfoliating 2D layers and so on.

import codecs
import copy  # 引用这个模块主要的作用是为了将输入的动态变量进行深拷贝，以防止在函数运行过程中的一些操作改变了输入的动态变量
import numpy as np
from os import path

default_directory = path.dirname(__file__)+'/'  # 设置这个代码文件所在的文件夹为默认读取路径

class latte:
    """ LATTicE operation """
    def __init__(self):
        self.name = latte

    # 这个函数可以读取指定POSCAR文件中的信息
    # 应注意，目前可读的POSCAR需要是VESTA生成.vasp文件格式，若需读取其他格式POSCAR则需对这个包进行扩展
    def ReadPOSCAR(self,POSCAR=default_directory+'POSCAR'):
        file = codecs.open(POSCAR,'rb','utf-8','ignore')  # Open file, using codecs to uniform coding type
        line = file.readline()
        lindex = 0  # line index
        lattice_vector = []  # lattice vector will be first append to this list
        atomic_coordinate = []  # the coordinates of all atoms will be first append to this list
        while line:
            if lindex == 0:
                system = line.strip()  # The string indicating the name of this system
            elif lindex == 1:
                scale = float(line.strip())  # The crystal structure will be scale by this parameter
            elif lindex >= 2 and lindex <=4:
                lattice_vector.append(list(map(float,line.split())))
            elif lindex == 5:
                atomic_species = list(map(str,line.split()))  # 原子种类
            elif lindex == 6:
                num_atom = list(map(int,line.split()))  # 各种类原子的数目
            elif lindex == 7:
                coordinate = line.strip()  # The type of coordinate system: Direct (fractional coordinate), Cartesian, ......
            else:
                atomic_coordinate.append(list(map(float,line.split())))

            line = file.readline()
            lindex += 1
        file.close()

        lattice_vector = np.array(lattice_vector)  # lattice vectors will be then transformed into a 3-dimensional array
        atomic_position = {'atomic_species':atomic_species,'num_atom':num_atom,'atomic_coordinate':atomic_coordinate}
        # The position of each atom will be preserved in this dictionary
        crystal_info = {'system':system,'scale':scale,'coordinate':coordinate}  # The information of this crystal will be preserved in this dictionary

        return lattice_vector,atomic_position,crystal_info  # 应注意：lattice_vector为数组，而atomic_position、crystal_info为字典

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

    # This function is designed to create new set of lattice vectors and atomic positions for supercell
    # size变量应为list类型
    def Supercell(self,scale_factor=[1,1,1],lattice_vector=None,atomic_position=None):
        s_x,s_y,s_z = scale_factor  # 解压出各个晶向上的增大倍数
        shrink_factor = [1/float(s_x),1/float(s_y),1/float(s_z)]  # 用于缩放原子坐标的缩放因子

        # 在python中，字符串、数值、元组均为静态变量，字典、列表为动态变量，所以对动态变量进行操作时要注意先将其深拷贝一份，以防止原动态变量中的值被改变
        # https://www.runoob.com/w3cnote/python-variable-references-and-copies.html
        # https://zhuanlan.zhihu.com/p/109563649
        # 接下来，我们按照顺序，先改晶格基矢再改原子坐标信息
        lattice_vector_old = copy.deepcopy(lattice_vector)  # # 深拷贝输入的列表变量，以防止后续操作改变输入列表中的值
        # 将旧的晶格基矢赋给新的变量，以防止互相影响，然后计算得到扩胞后的lattice vector
        lattice_vector_new = np.array([np.array(lattice_vector_old[n])*scale_factor[n] for n in range(len(lattice_vector_old))])
        # numpy数组乘以一个数，表示原数组中每个数字与这个数相乘 (input: np.array([1,2,3])*5, output: array([5,10,15]))

        atomic_position_new = copy.deepcopy(atomic_position)  # 深拷贝输入的字典变量，以防止后续操作改变输入字典中的值
        num_atom_old = atomic_position_new['num_atom']  # 提取扩胞前的原子总数
        atomic_coordinate_old = atomic_position_new['atomic_coordinate']  # 提取扩胞前的原子坐标

        # 先修改原子总数
        total_scale = s_x * s_y * s_z  # 原子总数增加的倍数
        num_atom_new = np.array(num_atom_old) * total_scale  # 修改各种类的原子总数一项
        atomic_position_new['num_atom'] = num_atom_new

        # 再修改原子坐标
        # 为了减少计算量，我们可以采用先对原本的原子进行缩放再平移（应注意，这样做使用的平移向量也需要进行对应的缩放）
        translation_basis = [1/float(s_x),1/float(s_y),1/float(s_z)]  # 先对平移的基矢进行缩放，设原晶格基矢为一，缩放后的基矢应当刚好等于缩放因子（shrink factor）
        t_x,t_y,t_z = translation_basis
        translation_vectors = []
        for i in range(s_x):
            for j in range(s_y):
                for k in range(s_z):
                    translation_vectors.append(np.array([i*t_x,j*t_y,k*t_z]))

        atomic_coordinate_new = []
        for n in range(len(atomic_coordinate_old)):
            origin_atom = np.array(atomic_coordinate_old[n])*np.array(shrink_factor)
            for m in range(len(translation_vectors)):
                atomic_coordinate_new.append(origin_atom+translation_vectors[m])

        atomic_position_new['atomic_coordinate'] = atomic_coordinate_new

        return lattice_vector_new,atomic_position_new


    def Exfoliate(self,vacuum_layer=20,lattice_vector=None,atomic_position=None):
        t_vac = vacuum_layer  # 真空层厚度

        # 同样，先修改晶格基矢，再修改原子坐标
        lattice_vector_new = copy.deepcopy(lattice_vector)
        z_a,z_b,z_c = lattice_vector_new[2]  # 解压出z晶向在正交直角坐标系下的三个分量
        lattice_vector_new[2] = np.array([z_a,z_b,z_c/2.0+t_vac])
        # 延长z晶向的长度，因为注意，由于我们接下来会删除一半的晶胞，所以延长后的长度应该是原本半个晶胞的长度加上真空层的厚度

        # 修改原子坐标
        atomic_position_new = copy.deepcopy(atomic_position)
        num_atom_old = atomic_position_new['num_atom']  # 提取剥离前的原子总数
        atomic_coordinate_old = atomic_position_new['atomic_coordinate'] # 提取剥离前的原子坐标

        # 先修改原子总数
        num_atom_new = [int(num_atom_old[i]/2.0) for i in range(len(num_atom_old))]  # 各种原子的数目减少为原先的一半，同时要注意转换为整型，不然Vesta读不了
        atomic_position_new['num_atom'] = num_atom_new

        # 再修改原子坐标
        atomic_coordinate_new = []
        for i in range(len(atomic_coordinate_old)):
            coord = atomic_coordinate_old[i]  # 将逐个原子坐标提取出来修改z方向的值
            if coord[2] <= 1/2:    # 判断这个原子属于上层还是下层，因为之前原子坐标采用的都是分数坐标，所以要用1/2来判断上下层
                coord[2] = (coord[2]*z_c+t_vac/2.0)/float(z_c/2.0+t_vac)  # 下层原子：先转换成正交直角坐标系下的坐标往上移动半个真空层再用延长后的z轴长度得到分数坐标
                atomic_coordinate_new.append(coord)
            else:
                pass  # 删除上层原子

        atomic_position_new['atomic_coordinate'] = atomic_coordinate_new

        return lattice_vector_new,atomic_position_new

    # 这个函数可用于得到特定厚度得二维材料（TMD适用）
    def ExfoliateFewLayer(self,num_layer=1,vacuum_layer=20,lattice_vector=None,atomic_position=None):
        # 对于TMD而已，一个晶胞中有两层monolayer，而我们的Exfoliate函数会将一层删除并保留一层
        # 所以如果我们想要n_layer层材料，我们可以先扩胞到n_cell=n_layer，再Exfoliate（该函数会将不要的那几层删除）
        lattice_vector_supercell,atomic_position_supercell = self.Supercell([1,1,int(num_layer)],lattice_vector,atomic_position)
        lattice_vector_new,atomic_position_new = self.Exfoliate(vacuum_layer,lattice_vector_supercell,atomic_position_supercell)
        return lattice_vector_new,atomic_position_new

    def Exfoliate2(self,num_layer=1,vacuum_layer=20,lattice_vector=None,atomic_position=None):
        latt_vec, atom_pos = self.Supercell([1,1,num_layer],lattice_vector,atomic_position)

        lattice_vector_new = copy.deepcopy(latt_vec)
        z_a, z_b, z_c = lattice_vector_new[2]  # 解压出z晶向在正交直角坐标系下的三个分量
        lattice_vector_new[2] = np.array([z_a, z_b, z_c+vacuum_layer])

        # shifting_vec = np.float(vacuum_layer)/np.float(z_c+vacuum_layer)
        atomic_position_new = copy.deepcopy(atom_pos)
        num_atom_new = atomic_position_new['num_atom']  # 提取剥离前的原子总数
        atomic_coordinate_new = atomic_position_new['atomic_coordinate']  # 提取剥离前的原子坐标
        for n in range(len(atomic_coordinate_new)):
            print(atomic_coordinate_new[n])
            a,b,c = atomic_coordinate_new[n]
            if c >= 0.5:
                atomic_coordinate_new[n] = [a,b,np.float(c*z_c+vacuum_layer)/np.float(z_c+vacuum_layer)]
            else:
                atomic_coordinate_new[n] = [a,b,np.float(c*z_c)/np.float(z_c+vacuum_layer)]
            print(atomic_coordinate_new[n])

        atomic_position_new['atomic_coordinate'] = atomic_coordinate_new

        return lattice_vector_new,atomic_position_new



#if __name__=='__main__':
    #pass
    #POSCAR = 'D:/MaterialsGallery/2D Materials/MoS2/Crystal structures/Bulk 2H-MoS2.vasp'
    #saving_directory = 'D:/MaterialsGallery/2D Materials/MoS2/Crystal structures/monolayer_2H_MoS2_new.vasp'
    #lt = latte()
    #crystal_intel = lt.ReadPOSCAR(POSCAR)
    #a,b,c = crystal_intel
    #a1,b1 = lt.Supercell([8,6,2],a,b)
    #print(a1)
    #print(b1)
    #print(a)
    #print(b)
    #print(c)
    #a1,b1 = lt.Exfoliate(20,a,b)
    #lt.WritePOSCAR(saving_directory,a1,b1,c)





