import numpy as np
from Wheels import GetData
from Wheels import functions
import matplotlib.pyplot as plt

f = functions.fx()
gd = GetData.geda()

def tan(a1,b1,a2,b2): return (b2-b1)/(a2-a1)
def b(x1,y1,x2,y2): return (y1*x2-y2*x1)/(x2-x1)

NA = 6.022e+23

P, Tao, Tab, Tob = [], [], [], []

for i in ['alpha','beta','omega']:
    if i == 'alpha':
        na = 2
    elif i == 'beta':
        na = 1
    elif i == 'omega':
        na = 3
    energy = gd.GetBindingEnergy('/Users/liusongwei/Titanium/binding-energy/binding-energy_3.0/'+i+'_binding-energy')
    locals()['E_'+str(i)] = energy[1]*NA*1.6e-19/na

for i in ['0', '20', '40', '60', '80', '100', '120', '140', '160', '180', '200', '220', '240', '260', '280', '300']:
    for j in ['alpha', 'beta', 'omega']:
        pdos = gd.GetPDOS('/Users/liusongwei/Titanium/data/data_fdm_3.0/'+j+'_dos/total_dos_'+j+'_'+i+'.dat')
        w_list = []
        p_list = []
        for k in range(len(pdos[:,0])):
            if pdos[k,0] > 0:
                w_list.append(pdos[k,0])
                p_list.append(pdos[k,1])
        locals()['w_'+str(j)] = np.array(w_list)
        locals()['p_'+str(j)] = np.array(p_list)
    P.append(np.float(i)/10)
    Tao.append(f.TransTemp(E_alpha[np.int(i)/20],p_alpha,w_alpha,E_omega[np.int(i)/20],p_omega,w_omega))
    Tab.append(f.TransTemp(E_alpha[np.int(i)/20],p_alpha,w_alpha,E_beta[np.int(i)/20],p_beta,w_beta))
    Tob.append(f.TransTemp(E_omega[np.int(i)/20],p_omega,w_omega,E_beta[np.int(i)/20],p_beta,w_beta))

P0, T1, T2 = [], [], []
for i in range(16):
    if i < 5:
        P0.append(P[i])
        T1.append(Tao[i])
        T2.append(Tab[i])
    elif i == 5:
        p1 = (b(P[4],Tab[4],P[5],Tab[5])-b(P[4],Tao[4],P[5],Tao[5]))/(tan(P[4],Tao[4],P[5],Tao[5])-tan(P[4],Tab[4],P[5],Tab[5]))
        p2 = (b(P[4],Tab[4],P[5],Tab[5])-b(P[4],Tob[4],P[5],Tob[5]))/(tan(P[4],Tob[4],P[5],Tob[5])-tan(P[4],Tab[4],P[5],Tab[5]))
        p3 = (b(P[4],Tob[4],P[5],Tob[5])-b(P[4],Tao[4],P[5],Tao[5]))/(tan(P[4],Tao[4],P[5],Tao[5])-tan(P[4],Tob[4],P[5],Tob[5]))
        p = (p1+p2+p3)/3
        t1 = (tan(P[4],Tao[4],P[5],Tao[5])*b(P[4],Tab[4],P[5],Tab[5])-tan(P[4],Tab[4],P[5],Tab[5])*b(P[4],Tao[4],P[5],Tao[5]))/(tan(P[4],Tao[4],P[5],Tao[5])-tan(P[4],Tab[4],P[5],Tab[5]))
        t2 = (tan(P[4],Tob[4],P[5],Tob[5])*b(P[4],Tab[4],P[5],Tab[5])-tan(P[4],Tab[4],P[5],Tab[5])*b(P[4],Tob[4],P[5],Tob[5]))/(tan(P[4],Tob[4],P[5],Tob[5])-tan(P[4],Tab[4],P[5],Tab[5]))
        t3 = (tan(P[4],Tao[4],P[5],Tao[5])*b(P[4],Tob[4],P[5],Tob[5])-tan(P[4],Tob[4],P[5],Tob[5])*b(P[4],Tao[4],P[5],Tao[5]))/(tan(P[4],Tao[4],P[5],Tao[5])-tan(P[4],Tob[4],P[5],Tob[5]))
        t = (t1+t2+t3)/3
        P0.append(p)
        T1.append(t)
        T2.append(t)
    else:
        P0.append(P[i])
        T1.append(Tob[i])
        T2.append(Tob[i])

plt.plot(P0,T1,color='b')
plt.plot(P0,T2,color='b')
plt.xlim(0,30)
plt.ylim(0,2000)
plt.text(3,1100,r'$\alpha$',fontsize='15')
plt.text(15,500,r'$\omega$',fontsize='15')
plt.text(20,1650,r'$\beta$',fontsize='15')
plt.xlabel(r'P (GPa)',fontsize='15')
plt.ylabel(r'T (K)',fontsize='15')

print(p,t)

#plt.plot(P,Tao,color='b')
#plt.plot(P,Tab,color='g')
#plt.plot(P,Tob,color='r')
plt.show()
plt.savefig('/Users/liusongwei/Desktop/P-T_phase_diagram_test.png')