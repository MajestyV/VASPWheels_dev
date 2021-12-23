# This code is written for extracting electronic band structure data from V.A.S.P. results.

import codecs
import re

class Ebands:
    def __init__(self):
        self.name = Ebands

    # This function is designed to extract electronic bands data from file EIGENVAL.
    def GetData(self,EIGENVAL):
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

if __name__=='__main__':
    EIGENVAL = 'D:/MaterialsGallery/Testing/MoS2_pawlda/MoS2_2H/1/result/EIGENVAL'
    ebands = Ebands()
    # Gamma-M-K-Gamma-A-L-H-A
    a = ebands.GetData(EIGENVAL)
    #print(len(a['energy'][0]))
    #print(len(a['occupation'][31]))
    print(a)
    #kpath.GetKpath(saving_directory,path,59)