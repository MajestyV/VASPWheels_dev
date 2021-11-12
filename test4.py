import numpy as np
from Wheels import GetData
from Wheels import functions

gd = GetData.geda()
f = functions.fx()

for i in ['alpha', 'omega']:
    locals()['V_'+str(i)] = []
    for j in ['minus', 'plus', 'orig']:
        DataPath = '/Users/liusongwei/Titanium/mode_Gruneisen_parameters/G_relaxed_structure_test1/'+i+'/POSCAR_unitcell_'+j
        par = gd.GetStructure(DataPath)
        V = f.Volume(par[0],par[1])*gd.GetStructure(DataPath)[2]
        locals()['V_'+str(i)].append(V)

difference1 = (V_alpha[2]-V_alpha[1])/(V_alpha[1])
difference2 = (V_omega[2]-V_omega[1])/(V_omega[1])

print(V_alpha, V_omega, difference1, difference2)

a = 14.10
b = 17.04
x = ((b/a)**2/3-1)/2

print(x)