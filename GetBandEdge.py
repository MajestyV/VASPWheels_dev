import matplotlib.pyplot as plt
from VaspWheels import GetEbands
from VaspWheels import GetKpath

GB = GetEbands.Ebands()
GK = GetKpath.Kpath()

EIGENVAL = 'D:/MaterialsGallery/Testing/MoS2_pawpbe/MoS2_2H/2/result_D2_ISIF4/EIGENVAL'
Bands = GB.GetData(EIGENVAL)
energy = Bands['energy']
K_path = Bands['kpath']
#print(len(a['energy'][0]))
#print(len(a['occupation'][31]))
print(len(energy))
print(len(energy[0]))
print(len(K_path))
#kpath.GetKpath(saving_directory,path,59)

# Gamma-M-K-Gamma
path = [[0, 0, 0], [0.5, 0, 0], [1.0 / 3.0, 1.0 / 3.0, 0], [0, 0, 0]]
#a = kpath.Kgenerator(path,59)
projected_path = GK.ProjectKpath(path,59,LatticeCorrection='True',Lattice=['HEX', [3.16, 3.16, 12.9, 90, 90, 120], 'primitive'])
print(len(projected_path[0]))
print((projected_path[1]))

Efermi = -0.8
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

VBM = [max(Valence[i]) for i in range(len(Valence))]
CBM = [min(Conductive[i]) for i in range(len(Conductive))]

#plt.plot(projected_path[0],VBM)
#plt.plot(projected_path[0],CBM)

print(max(VBM))
print(min(CBM))