import numpy as np
from Wheels import GetData
from Wheels import functions
import matplotlib.pyplot as plt

f = functions.fx()
gd = GetData.geda()

NA = 6.022e+23
E_alpha = -7.950*NA*1.6e-19
E_beta = -7.838*NA*1.6e-19
E_omega = -7.955*NA*1.6e-19

P, Tao, Tab, Tob = [], [], [], []
#for i in ['0', '20', '40', '60', '80', '100', '120', '140', '160', '180', '200', '220', '240', '260', '280', '300']:
for i in ['0', '20', '40', '60', '80', '100', '120']:
    for j in ['alpha', 'beta', 'omega']:
        pdos = gd.GetPDOS('/Users/liusongwei/Titanium/data/data_test/'+j+'_dos/total_dos_'+j+'_'+i+'.dat')
        w_list = []
        p_list = []
        for k in range(len(pdos[:,0])):
            if pdos[k,0] > 0:
                w_list.append(pdos[k,0])
                p_list.append(pdos[k,1])
        locals()['w_'+str(j)] = np.array(w_list)
        locals()['p_'+str(j)] = np.array(p_list)
    P.append(np.float(i)/10)
    Tao.append(f.TransTemp(E_alpha,p_alpha,w_alpha,E_omega,p_omega,w_omega))
    Tab.append(f.TransTemp(E_alpha,p_alpha,w_alpha,E_beta,p_beta,w_beta))
    Tob.append(f.TransTemp(E_omega,p_omega,w_omega,E_beta,p_beta,w_beta))

plt.plot(P,Tao,color='b')
plt.plot(P,Tab,color='g')
plt.plot(P,Tob,color='r')
plt.show()
plt.savefig('/Users/liusongwei/Desktop/P-T_phase_diagram_test.png')