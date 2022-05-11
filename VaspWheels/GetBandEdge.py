import matplotlib.pyplot as plt
from VaspWheels import GetEbands
from VaspWheels import GetKpath
import re
import codecs

GE = GetEbands.Ebands()
GK = GetKpath.Kpath()

class BandEdge:
    """ This class of function is written for analyzing band gaps of semiconductors or insulators. """
    def __init__(self):
        self.name = BandEdge

    # Markdown_SCF记载着准确的费米能级
    def GetEfermi(self,Markdown_SCF,deviation=0):
        pattern = re.compile(r'-?\d+\.?\d+')  # 匹配浮点数的正则表达式
        f = codecs.open(Markdown_SCF, 'rb', 'utf-8', 'ignore')
        line = f.readline()
        Energy = pattern.findall(line)
        # print(Energy)
        Efermi = float(Energy[0])+deviation
        return Efermi

    # 这个函数通过占据情况来找出导带跟价带，以确定半导体带隙
    def GetBandEdge(self,EIGENVAL):
        Bands =GE.GetData(EIGENVAL)        # 用之前的函数包从EIGENVAL文件提取能带数据
        energy = Bands['energy']           # 获取能带数据
        K_path = Bands['kpath']            # 获取计算EIGENVAL时的K空间路径
        occupation = Bands['occupation']   # 获取能带占据信息

        Conductive = []   # 这个列表用于存放所有未被占据的能带数据
        Valence = []      # 这个列表用于存放所有已被占据的能带数据
        for n in range(len(K_path)):
            E_c = []
            E_v = []
            for m in range(len(energy)):
                E = energy[m][n]
                filled = occupation[m][n]
                if round(filled,0) == 0:    # 通过判断能带的占据情况来确定能带在费米面之下还是费米面之上
                    E_c.append(E)
                else:
                    E_v.append(E)
            Conductive.append(E_c)
            Valence.append(E_v)

        Valence_Band = [max(Valence[i]) for i in range(len(Valence))]           # 最低未占据能带，Lowest unoccupied band
        Conduction_Band = [min(Conductive[i]) for i in range(len(Conductive))]  # 最高已占据能带，Highest occupied band

        return Valence_Band, Conduction_Band

    # 与上面的函数不同，这个函数通过费米面来判断导带价带的位置（不太准确）
    def GetBandEdge_2(self,EIGENVAL,Efermi):
        Bands = GE.GetData(EIGENVAL)
        energy = Bands['energy']
        K_path = Bands['kpath']

        Conductive = []
        Valence = []
        for n in range(len(K_path)):
            E_c = []
            E_v = []
            for m in range(len(energy)):
                E = energy[m][n]
                # print(E)
                if E >= Efermi:
                    E_c.append(E)
                else:
                    E_v.append(E)
            Conductive.append(E_c)
            Valence.append(E_v)

        Valence_Band = [max(Valence[i]) for i in range(len(Valence))]
        Conduction_Band = [min(Conductive[i]) for i in range(len(Conductive))]

        return Valence_Band, Conduction_Band

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