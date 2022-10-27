import re
import codecs
from VaspWheels import GetEbands
from VaspWheels import GetKpath

GE = GetEbands.Ebands()  # 调用GetEbands模块
GK = GetKpath.Kpath()    # 调用GetKpath模块

class Bandgap:
    """ This class of function is written for analyzing band gaps based on the result calculated by V.A.S.P.. """
    def __init__(self):
        self.name = Bandgap

    # Markdown_SCF记载着准确的费米能级
    def GetEfermi(self,Markdown_SCF,deviation=0):
        pattern = re.compile(r'-?\d+\.?\d+')  # 匹配浮点数的正则表达式
        f = codecs.open(Markdown_SCF, 'rb', 'utf-8', 'ignore')
        line = f.readline()
        Energy = pattern.findall(line)
        # print(Energy)
        Efermi = float(Energy[0])+deviation
        return Efermi

    # 此函数通过能带占据情况区分导带跟价带
    # 由于DFT算法本身的原因，会出现轨道分数占据的情况，所以我们使用OrderPrecision控制占据情况的精确度
    # 如OrderPrecision=2，则精确到小数点后两位
    def AnalyzeOccupation(self,EIGENVAL,Precision=0):
        Bands =GE.GetData(EIGENVAL)        # 利用GetEbands模块从EIGENVAL文件提取能带数据
        energy = Bands['energy']           # 获取能带数据
        K_path = Bands['kpath']            # 获取计算EIGENVAL时的K空间路径
        occupation = Bands['occupation']   # 获取能带占据信息

        Unoccupied = []   # 这个列表用于存放所有未被占据的能带数据
        Occupied = []      # 这个列表用于存放所有已被占据的能带数据
        for n in range(len(K_path)):
            E_unoccupied = []
            E_occupied = []
            for m in range(len(energy)):
                E = energy[m][n]
                filling_condition = occupation[m][n]  # 电子的填充情况
                if round(filling_condition,Precision) == 0:    # 通过判断能带的占据情况来确定能带在费米面之下还是费米面之上
                    E_unoccupied.append(E)
                else:
                    E_occupied.append(E)
            Unoccupied.append(E_unoccupied)
            Occupied.append(E_occupied)

        ConductionBand = [min(Unoccupied[i]) for i in range(len(Unoccupied))]  # 最低未占据能带（导带），Lowest unoccupied band
        ValenceBand = [max(Occupied[i]) for i in range(len(Occupied))]         # 最高已占据能带（价带），Highest occupied band

        return ValenceBand, ConductionBand

    # 此函数通过费米能级的位置区分导带跟价带（不太准确）
    def AnalyzeEfermi(self,EIGENVAL,Efermi=0):
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
    def AnalyzeBandgap(self,EIGENVAL,**kwargs):
        mode = kwargs['mode'] if 'mode' in kwargs else 'Occupation'      # 默认通过电子占据情况分析带隙
        Precision = kwargs['Precision'] if 'Precision' in kwargs else 0  # 分析电子占据情况时所用的精确度
        Efermi = kwargs['Efermi'] if 'Efermi' in kwargs else 0.0         # 通常不使用此模式，故设Efermi为0

        if mode == 'Occupation':
            ValenceBand, ConductionBand = self.AnalyzeOccupation(EIGENVAL,Precision=Precision)
        elif mode == 'Efermi':
            ValenceBand, ConductionBand = self.AnalyzeEfermi(EIGENVAL, Efermi=Efermi)
        else:
            print(r'ERROR: The mode of this function could only be "Occupation" or "Efermi".')
            return

        Ev_max = max(ValenceBand)     # 价带顶
        Ec_min = min(ConductionBand)  # 导带底
        Eg = Ec_min-Ev_max            # 带隙

        # 分析价带顶跟导带底的位置
        extremum_position = (ValenceBand.index(Ev_max),ConductionBand.index(Ec_min))

        return Eg,Ev_max,Ec_min,extremum_position

if __name__=='__main__':
    BE = BandEdge()

    EIGENVAL = 'D:/Projects/PhaseTransistor/Data/Simulation/GSE/3/3_D3BJ_GSE_1/0.225/EIGENVAL'

    # Markdown = 'D:/Data/MoS2/GSE/pawpbe_vasp5_SOC/2/2_D2ISIF4_GSE/Iterative_SettingTest2/0.280/Markdown_SCF'  # 这个文件记载着准确的费米能级
    # Efermi = BE.GetEfermi(Markdown,0.1)

    vb,cb = BE.GetBandEdge(EIGENVAL)
    print(vb,cb)
    print(max(vb),min(cb))
    print(min(cb)-max(vb))

    x = range(len(vb))
    plt.plot(x,vb)
    plt.plot(x,cb)