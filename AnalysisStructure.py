import numpy as np
import codecs

#Bulk_struc = '/Users/liusongwei/MaterialsGallery/MoS2/Data/MoS2_POSCAR/MoS2_bulk.vasp'
#Initial_struc = '/Users/liusongwei/MaterialsGallery/MoS2/Data/MoS2_POSCAR/MoS2_2.vasp'
#D2_ISIF2 = '/Users/liusongwei/MaterialsGallery/MoS2/Data/MoS2_2H_pawpbe/result_D2_ISIF2/relaxed_structure'
#noD2_ISIF2 = '/Users/liusongwei/MaterialsGallery/MoS2/Data/MoS2_2H_pawpbe/result_noD2_ISIF2/relaxed_structure'
#D2_ISIF4 = '/Users/liusongwei/MaterialsGallery/MoS2/Data/MoS2_2H_pawpbe/result_D2_ISIF4/relaxed_structure'
#noD2_ISIF4 = '/Users/liusongwei/MaterialsGallery/MoS2/Data/MoS2_2H_pawpbe/result_noD2_ISIF4/relaxed_structure'

input = '/Users/liusongwei/MaterialsGallery/MoS2/Data/MoS2_2H/MoS2_pawpbe_vasp5_SOC/bulk/bulk_D3BJ/relaxed_structure'
#bulk_33 = '/Users/liusongwei/MaterialsGallery/MoS2/Data/MoS2_2H/MoS2_pawlda_SOC/bulk/result_DoubleRelax_ISIF3-3/relaxed_structure'

# This function is written to read the CONTCAR (relaxed_structure) and analysis the data within.
def GetStructure(CONTCAR):
    file = codecs.open(CONTCAR, 'rb', 'utf-8', 'ignore')
    line = file.readline()
    lindex = 0
    lattice_parameter = []
    atomic_position_raw = []
    while line:
        content = line.split()  # 以空字符（空格，换行'\n'，制表符'\t'等）为分隔符对本行内容做切片 （什么都不填默认为空字符）
        if lindex == 0:
            system = line.split()
        elif lindex == 1:
            scale = float(content[0])
        elif lindex >= 2 and lindex <= 4:
            content = list(map(float,content))
            lattice_parameter.append(content)
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

    structure = {'system':system, 'scale':scale,
                 'atom': atom_species, 'num_atom':num_atom,
                 'coordinate_system':coordinate,
                 'lattice_parameter':lattice_parameter,
                 'atomic_position':atomic_position}
    return structure

# 用于计算不同晶体坐标下的原子间距
def distance(Point_1, Point_2, latt_param=[[1.0,0,0],[0,1.0,0],[0,0,1.0]]):
    a1, a2, a3 = latt_param
    latt = np.mat([a1,a2,a3])
    latt_T = np.transpose(latt)
    MetricTensor = np.dot(latt,latt_T)  # 应注意，这里要用向量/矩阵的点乘，不是叉乘，不要弄混

    d_vec = np.mat(Point_1)-np.mat(Point_2)
    d_sqaure = d_vec*MetricTensor*np.transpose(d_vec)  # 同时，这里也是点乘
    d_sqaure = np.array(d_sqaure)  # 将d_square从矩阵形式转变为数组形式

    return np.sqrt(d_sqaure[0][0])

def Structure_of_MoS2(relaxed_structure,m=3):
    Sturc_info = GetStructure(relaxed_structure)
    lp = Sturc_info['lattice_parameter']  # lp - lattice parameter
    atom_pos = Sturc_info['atomic_position']
    natom = Sturc_info['num_atom']

    a_vec, b_vec, c_vec = lp
    a = np.linalg.norm(np.array(a_vec),ord=2)  # 二范数即向量的模
    b = np.linalg.norm(np.array(b_vec),ord=2)


    #g = np.mat([a_vec,b_vec,c_vec])
    #g_T = np.transpose(g)
    #metric_tensor = np.dot(g,g_T)  # 应注意，这里要用向量/矩阵的点乘，不是叉乘，不要弄混
    #print(metric_tensor)

    num_Mo = int(natom[0])
    num_S = int(natom[1])
    Mo_1 = np.mat(atom_pos[0])
    Mo_2 = np.mat(atom_pos[1])
    S_1 = np.mat(atom_pos[num_Mo])
    S_2 = np.mat(atom_pos[num_Mo+1])
    S_3 = np.mat(atom_pos[num_Mo+2])
    S_4 = np.mat(atom_pos[num_Mo+3])

    a0 = round(distance([1.0,0,0],[0,0,0],lp),m)
    b0 = round(distance([0,1.0,0],[0,0,0],lp),m)
    c0 = round(distance([0,0,1.0],[0,0,0],lp),m)
    c_over_2 = round(distance([0,0,np.array(Mo_1)[0][2]],[0,0,np.array(Mo_2)[0][2]],lp),m)
    d_Mo1_S1 = round(distance(Mo_1,S_1,lp),m)
    d_Mo1_S2 = round(distance(Mo_1,S_2,lp),m)
    d_Mo1_S3 = round(distance(Mo_1,S_3,lp),m)
    d_Mo1_S4 = round(distance(Mo_1,S_4,lp),m)
    d_Mo2_S1 = round(distance(Mo_2,S_1,lp),m)
    d_Mo2_S2 = round(distance(Mo_2,S_2,lp),m)
    d_Mo2_S3 = round(distance(Mo_2,S_3,lp),m)
    d_Mo2_S4 = round(distance(Mo_2,S_4,lp),m)

    return a0, b0, c0, c_over_2, [d_Mo1_S1,d_Mo1_S2,d_Mo1_S3,d_Mo1_S4], [d_Mo2_S1,d_Mo2_S2,d_Mo2_S3,d_Mo2_S4]

for data in [input]:
    a, b, c, inter_spacing, dMo1, dMo2 = Structure_of_MoS2(data)
    print(str(data)+':')
    print(a,b,c)
    print(inter_spacing)
    print(dMo1,dMo2)
