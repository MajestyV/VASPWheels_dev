import numpy as np

from VaspWheels import LatticeOperation

LO = LatticeOperation.latte()

# data_directory = 'D:/PhD_research/Data/Simulation/MoS2/CarrierTransport/4/ort_supercell/manual_optimization/'

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
# data_directory = 'D:/Projects/PhaseTransistor/Data/Simulation/Conductivity/Strain/Structures/4_025x_y_strain/'
data_directory = 'D:/PhD_research/Data/Simulation/MoS2/CarrierTransport/4/Strain/Structures/4_LocalMinimum_x_strain/'

file_name = 'POSCAR0.000.vasp'

lattice_vector, atomic_position, crystal_info = LO.ReadPOSCAR(data_directory+file_name)

# strain = [-0.0050, -0.0025, 0.0025, 0.0050, 0.0075, 0.0100, 0.0125, 0.0150, 0.0175, 0.0200]
strain = [-0.060, -0.055, -0.050, -0.045, -0.040, -0.035, -0.030, -0.025, -0.020, -0.015, -0.010, -0.005, 0.000,
          0.005, 0.010, 0.015, 0.020, 0.025, 0.030, 0.035, 0.040, 0.045, 0.050, 0.055, 0.060]

for i in range(len(strain)):
    #scaling = np.array([[1+strain[i],1+strain[i],1+strain[i]],
                        #[1+np.sqrt(3)*strain[i],1+np.sqrt(3)*strain[i],1+np.sqrt(3)*strain[i]],
                        #[1,1,1]])
    # x strain
    #scaling = np.array([[1,1,1],
                        #[1+strain[i],1+strain[i],1+strain[i]],
                        #[1,1,1]])
    # y strain
    scaling = np.array([[1+strain[i],1+strain[i],1+strain[i]],
                        [1,1,1],
                        [1,1,1]])

    lattice_new = lattice_vector * scaling

    saving_file_name = 'POSCAR'+str("%.3f" %strain[i])+'.vasp'  # 浮点数转换为字符串时保留三位小数

    LO.WritePOSCAR(data_directory + saving_file_name, lattice_vector=lattice_new, atomic_position=atomic_position,
                   crystal_info=crystal_info)
