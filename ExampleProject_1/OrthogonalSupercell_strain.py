import numpy as np

from VaspWheels import LatticeOperation

LO = LatticeOperation.latte()

data_directory = 'D:/PhD_research/Data/Simulation/MoS2/CarrierTransport/4/ort_supercell/manual_optimization/'

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
file_name = 'POSCAR_strained.vasp'

lattice_vector, atomic_position, crystal_info = LO.ReadPOSCAR(data_directory+file_name)

strain = [-0.040, -0.035, -0.030, -0.025, -0.020, -0.015, -0.010, -0.005, 0.000, 0.005, 0.010, 0.015, 0.020, 0.025,
          0.030, 0.035, 0.040]

for i in range(len(strain)):
    scaling = np.array([[1, 1,1],
                        [1+strain[i],1+strain[i],1+strain[i]],
                        [1,1,1]])

    lattice_new = lattice_vector * scaling

    saving_file_name = 'POSCAR'+str(strain[i])+'.vasp'

    LO.WritePOSCAR(data_directory + saving_file_name, lattice_vector=lattice_new, atomic_position=atomic_position,
                   crystal_info=crystal_info)
