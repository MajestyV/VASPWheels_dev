from Wheels import GetData
import matplotlib.pyplot as plt

gd = GetData.geda()
path1 = '/Users/liusongwei/Titanium/mode_Gruneisen_parameters/result_fdm_G_test4_dfpt/omega/minus/band.yaml'
path2 = '/Users/liusongwei/Titanium/mode_Gruneisen_parameters/result_fdm_G_test4_dfpt/omega/orig/band.yaml'
path3 = '/Users/liusongwei/Titanium/mode_Gruneisen_parameters/result_fdm_G_test4_dfpt/omega/plus/band.yaml'
#print(gd.GetPhononBands(path))

phonon1 = gd.GetPhononBands(path1,x=5,y=0,z=5)
phonon2 = gd.GetPhononBands(path2,x=5,y=0,z=5)
phonon3 = gd.GetPhononBands(path3,x=5,y=0,z=5)

K = phonon1[2][1]
M = phonon1[2][2]
G = phonon1[2][3]

for i in range(phonon1[3]):
    if i == 0:
        plt.plot(phonon1[0],phonon1[1][:,i],color='b',linewidth=1,label=r'$V_0-\Delta$V')
    else:
        plt.plot(phonon1[0], phonon1[1][:, i], color='b', linewidth=1)
for i in range(phonon2[3]):
    if i == 0:
        plt.plot(phonon2[0],phonon2[1][:,i],color='g',linewidth=1,label=r'$V_0$')
    else:
        plt.plot(phonon2[0], phonon2[1][:, i], color='g', linewidth=1)
for i in range(phonon3[3]):
    if i == 0:
        plt.plot(phonon3[0],phonon3[1][:,i],color='r',linewidth=1,label=r'$V_0+\Delta$V')
    else:
        plt.plot(phonon3[0], phonon3[1][:, i], color='r', linewidth=1)
plt.xlim(phonon1[0][0],phonon1[0][phonon1[4]-1])
plt.ylim(0,9)
plt.xticks([])
plt.legend(loc='best')
plt.axvline(K,color='k',linewidth=1,linestyle=':')
plt.axvline(M,color='k',linewidth=1,linestyle=':')
plt.axvline(G,color='k',linewidth=1,linestyle=':')
plt.savefig('/Users/liusongwei/Desktop/bandstructure_omega.png')

#print(phonon1[0])