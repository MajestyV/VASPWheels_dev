import numpy as np
from Wheels import GetData
from Wheels import functions
import matplotlib.pyplot as plt

f = functions.fx()
gd = GetData.geda()

def BME(V,E0,V0,B0,dB0):
    a = (V0/V)**(2/3)
    Energy = E0 +9*V0*B0*(dB0*(a-1)**3+(6-4*a)*(a-1)**2)
    return Energy

for i in ['alpha', 'beta', 'omega']:
    par = gd.GetStructure('/Users/liusongwei/Titanium/crystal_structure/'+i+'_Ti.vasp')  # par for parameter
    V0 = f.Volume(par[0], par[1])
    E = gd.GetBindingEnergy('/Users/liusongwei/Titanium/binding-energy/binding-energy/'+i+'/'+i+'_binding-energy')
    locals()['V_' + str(i)] = []
    locals()['E_' + str(i)] = []
    for j in range(E[2]):
        locals()['V_'+str(i)].append(V0*E[0][j])
        locals()['E_'+str(i)].append(E[1][j]/par[1])

#V = np.linspace(14,20,200)
#plt.plot(V,BME(V,np.min(E_alpha),V_alpha[5],111.4,3.5))
#plt.plot(V,BME(V,np.min(E_beta),V_beta[5],106.3,3.3))
#plt.plot(V,BME(V,np.min(E_omega),V_omega[5],111.5,3.5))
plt.plot(V_alpha,E_alpha,color='b',label=r'$\alpha$')
plt.plot(V_beta,E_beta,color='g',label=r'$\beta$')
plt.plot(V_omega,E_omega,color='r',label=r'$\omega$')
plt.legend(loc = 'best')
plt.xlim(16,19)
plt.ylim(-7.80,-7.40)
plt.xlabel(r'Volume ($A^3$)',fontsize='15')
plt.ylabel(r'Energy (eV/atom)',fontsize='15')
plt.show()
#plt.savefig('/Users/liusongwei/Desktop/Zero_kelvin_total_energy_test.png')