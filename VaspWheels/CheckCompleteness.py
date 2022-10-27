import re
import codecs
import numpy as np
from VaspWheels import AnalyzeBandgap

AB = AnalyzeBandgap.Bandgap()  # 调用AnalyzeBandgap模块

class check:
    """This class of function is designed for checking the completeness of data obtained by V.A.S.P. calculation."""
    def __init__(self):
        self.name = check

    def Check_GSE_Data(self,data_point, home_directory, file_list=('output_SCF', 'output_DOS', 'output_Ebands')):
        beacon = '   1 F= '  # 计算正常进行的标志
        result = np.zeros((len(data_point), len(file_list)))
        for i in data_point:
            for j in file_list:
                log_file = home_directory + '/' + i + '/result/' + j  # 日志文件的地址
                f = codecs.open(log_file, 'rb', 'utf-8', 'ignore')
                line = f.readline()
                indicator = 0  # 复位
                while line:
                    if re.match(beacon, line) != None:
                        indicator += 1
                    else:
                        pass
                    line = f.readline()
                f.close()
                result[data_point.index(i), file_list.index(j)] = indicator
        return result

    def Extract_Fermi_energy(self,data_point, home_directory):
        E_fermi = []
        for n in data_point:
            Markdown = home_directory + '/' + n + '/Markdown_SCF'  # 这个文件记载着准确的费米能级
            pattern = re.compile(r'-?\d+\.?\d+')  # 匹配浮点数的正则表达式
            f = codecs.open(Markdown, 'rb', 'utf-8', 'ignore')
            line = f.readline()
            Energy = pattern.findall(line)
            E_fermi.append(float(Energy[0]))
        return E_fermi

    def Extract_GSE_Data(self,data_point, home_directory):
        Efield = []
        Bandgap = []
        for n in data_point:
            EIGENVAL = home_directory + '/' + n + '/EIGENVAL'

            VB, CB = AB.GetBandEdge(EIGENVAL)

            # print(n,min(CB)-max(VB))
            Efield.append(float(n))
            Bandgap.append(min(CB) - max(VB))

        return Efield, Bandgap

    def Extract_GSE_Data_2(self,data_point, home_directory, E_fermi):
        Efield = []
        Bandgap = []
        for n in data_point:
            EIGENVAL = home_directory + '/' + n + '/EIGENVAL'

            VB, CB = AB.GetBandEdge_2(EIGENVAL, E_fermi[data_point.index(n)])

            # print(n,min(CB)-max(VB))
            Efield.append(float(n))
            Bandgap.append(min(CB) - max(VB))

        return Efield, Bandgap

    def Extract_negative_GSE_Data(self,data_point, home_directory):
        Efield = []
        Bandgap = []
        for n in data_point:
            EIGENVAL = home_directory + '/' + n + '/EIGENVAL'

            VB, CB = AB.GetBandEdge(EIGENVAL)

            # print(n,min(CB)-max(VB))
            Efield.append(-float(n.replace('m', '')))
            Bandgap.append(min(CB) - max(VB))

        return Efield, Bandgap

    def Extract_negative_GSE_Data_2(self,data_point, home_directory, E_fermi):
        Efield = []
        Bandgap = []
        for n in data_point:
            EIGENVAL = home_directory + '/' + n + '/EIGENVAL'

            VB, CB = AB.GetBandEdge_2(EIGENVAL, E_fermi[data_point.index(n)])

            # print(n,min(CB)-max(VB))
            Efield.append(-float(n.replace('m', '')))
            Bandgap.append(min(CB) - max(VB))

        return Efield, Bandgap

    def reshape(self,x, y, critical_point):
        x_new = []
        y_new = []
        for i in range(len(x)):
            if x[i] >= critical_point:
                x_new.append(x[i])
                y_new.append(y[i])
            else:
                pass
        return x_new, y_new

    def FittedLine(self,x, Data_x, Data_y):
        slope, intercept, r_value, p_value, std_err = st.linregress(Data_x, Data_y)
        return slope * x + intercept