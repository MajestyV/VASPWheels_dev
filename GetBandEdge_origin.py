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

    def GetBandEdge(self,EIGENVAL,Efermi):
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
    EIGENVAL = 'D:/Data/MoS2/GSE/pawpbe_vasp5_SOC/2/2_D2ISIF4_GSE/Iterative_SettingTest2/0.280/EIGENVAL'

    Markdown = 'D:/Data/MoS2/GSE/pawpbe_vasp5_SOC/2/2_D2ISIF4_GSE/Iterative_SettingTest2/0.280/Markdown_SCF'  # 这个文件记载着准确的费米能级
    pattern = re.compile(r'-?\d+\.?\d+')  # 匹配浮点数的正则表达式
    f = codecs.open(Markdown, 'rb', 'utf-8', 'ignore')
    line = f.readline()
    Energy = pattern.findall(line)
    # print(Energy)
    Efermi = float(Energy[0])+0.1

    BE = BandEdge()
    vb,cb = BE.GetBandEdge(EIGENVAL,Efermi)
    print(vb,cb)
    print(max(vb),min(cb))
    print(min(cb)-max(vb))


#EIGENVAL = 'D:/MaterialsGallery/Testing/MoS2_pawpbe/MoS2_2H/2/result_D2_ISIF4/EIGENVAL'
#Bands = GB.GetData(EIGENVAL)
#energy = Bands['energy']
#K_path = Bands['kpath']
#print(len(a['energy'][0]))
#print(len(a['occupation'][31]))
#print(len(energy))
#print(len(energy[0]))
#print(len(K_path))
#kpath.GetKpath(saving_directory,path,59)

# Gamma-M-K-Gamma
#path = [[0, 0, 0], [0.5, 0, 0], [1.0 / 3.0, 1.0 / 3.0, 0], [0, 0, 0]]
#a = kpath.Kgenerator(path,59)
#projected_path = GK.ProjectKpath(path,59,LatticeCorrection='True',Lattice=['HEX', [3.16, 3.16, 12.9, 90, 90, 120], 'primitive'])
#print(len(projected_path[0]))
#print((projected_path[1]))

#Efermi = -0.8
#Conductive = []
#Valence = []
#for n in range(len(K_path)):
#    E_c = []
#    E_v = []
#    for m in range(len(energy)):
#        E = energy[m][n]
#        # print(E)
#        if E >= Efermi:
#            E_c.append(E)
#        else:
#           E_v.append(E)
#   Conductive.append(E_c)
#    Valence.append(E_v)

#VBM = [max(Valence[i]) for i in range(len(Valence))]
#CBM = [min(Conductive[i]) for i in range(len(Conductive))]

#plt.plot(projected_path[0],VBM)
#plt.plot(projected_path[0],CBM)

#print(max(VBM))
#print(min(CBM))