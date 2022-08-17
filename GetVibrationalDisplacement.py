import numpy as np
import yaml
import matplotlib.pyplot as plt

file = 'D:/Projects/PhaseTransistor/Data/Simulation/Phonon/4_D3BJ_FD_vdw/phonon/eigenvectors/band.yaml'

def ReadPhonopyData(band_yaml):
    with open(band_yaml) as f:
        data = yaml.load(f, Loader=yaml.FullLoader)
    return data

def RearrangeEigenvector(eigenvector_rawdata,natoms,degree_of_freedom):
    dim = int(natoms*degree_of_freedom)
    normal_coordinate = np.zeros((dim,dim))
    return

def GetGammaEigenvertor(band_yaml,degree_of_freedom=3):
    data = ReadPhonopyData(band_yaml)
    natoms = data['natom']
    Gamma = data['phonon'][0]
    k_point = Gamma['q-position']
    bands = Gamma['band']
    nbands = len(bands)  # num_bands = num_atoms * degree_of_freedom

    normal_coordinate = np.zeros((nbands,nbands))
    for n in range(nbands):
        eigenvector = bands[n]['eigenvector']
        for i in range(natoms):
            for j in range(degree_of_freedom):
                normal_coordinate[n][i*3+j] = eigenvector[i][j][0]  # 取实部

    return normal_coordinate, k_point, nbands

#a = GetGammaEigenvertor(file)

#print(a[0])