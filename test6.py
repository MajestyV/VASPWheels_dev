from Wheels import GetData
import matplotlib.pyplot as plt

gd = GetData.geda()
path1 = '/Users/liusongwei/Titanium/mode_Gruneisen_parameters/result_fdm_G_test4_dfpt/alpha/gruneisen.yaml'
path2 = '/Users/liusongwei/Titanium/mode_Gruneisen_parameters/result_fdm_G_test4_dfpt/omega/gruneisen.yaml'
#path3 = '/Users/liusongwei/Titanium/mode_Gruneisen_parameters/result_fdm_G_test1/alpha/plus/band.yaml'
#print(gd.GetPhononBands(path))

g1 = gd.GetGruneisen(path1)
#g2 = gd.GetGruneisen(path2)
#phonon2 = gd.GetPhononBands(path2,x=5,y=0,z=5)
#phonon3 = gd.GetPhononBands(path3,x=5,y=0,z=5)

K = g1[3][1]
M = g1[3][2]
G = g1[3][3]

for i in range(g1[4]):
    plt.plot(g1[0],g1[1][:,i],color='b',linewidth=1)
#for i in range(g2[4]):
    #plt.plot(g2[0],g2[1][:,i],color='b',linewidth=1)
plt.xlim(g1[0][0],g1[0][g1[5]-1])
plt.ylim(-1,5)
plt.axvline(K,color='k',linewidth=1,linestyle=':')
plt.axvline(M,color='k',linewidth=1,linestyle=':')
plt.axvline(G,color='k',linewidth=1,linestyle=':')
plt.savefig('/Users/liusongwei/Desktop/gruneisen_alpha.png')

#print(phonon1[0])