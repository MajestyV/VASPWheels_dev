import numpy as np
import matplotlib.pyplot as plt
from VaspWheels import GeneralAnalyzer

GA = GeneralAnalyzer.functions()  # 调用GeneralAnalyzer模块

data_directory = 'D:/PhD_research/Data/Simulation/MoS2/CarrierTransport/4/strain/Energy profile/'

file_name = ['4_005x_y_strain.dat', '4_010x_y_strain.dat', '4_015x_y_strain.dat',
             '4_020x_y_strain.dat', '4_025x_y_strain.dat']

strain_x = [0.005, 0.010, 0.015, 0.020, 0.025]

binding_energy = np.array(np.zeros((9,5))) # 创建一个二维数组存放数据
a = binding_energy

strain_y = np.array(np.zeros(9))
for i in range(len(file_name)):
    strain_y, energy = GA.GetData_txt(data_directory+file_name[i])
    binding_energy[:,i] = energy

X, Y = np.meshgrid(strain_x,strain_y)

print(X.shape)
print(Y.shape)
print(binding_energy.shape)

#def f(x,y):
    #a = list(x[0]).index
    #print(a)
    #b = list(y[0]).index
    #return binding_energy[a,b]

GA.Visualize3D_surface(X,Y,binding_energy)

plt.xlim(0.00,0.025)
plt.ylim(0.00,0.025)

##################################################################################################################
# file_name = 'POSCAR_PreRelax.vasp'

# lattice_vector, atomic_position, crystal_info = LO.ReadPOSCAR(data_directory+file_name)

#print(atomic_position)

#print(lattice_vector)
#lattice_vector = np.array(lattice_vector)

#strain = 0.01819120555655874

#scaling = np.array([[1+strain, 1+strain, 1+strain],
                    #[1,1,1],
                    #[1,1,1]])

#lattice_new = lattice_vector*scaling

#print(lattice_new)

#saving_file_name = 'POSCAR_strained.vasp'

#LO.WritePOSCAR(data_directory+saving_file_name,lattice_vector=lattice_new,atomic_position=atomic_position,crystal_info=crystal_info)

#####################################################################################################################