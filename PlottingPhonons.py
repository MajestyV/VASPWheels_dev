import codecs
import re
import matplotlib.pyplot as plt
from VaspWheels import GetPhonopyData

GPD = GetPhonopyData.Phonon()  # 能带可视化专用包

Data = {'Zero-field with vdw correction':'D:/Data/MoS2/Phonon/D3BJ_IBRION6/test_vdw/band.yaml',
        '0.25 V/nm with vdw correction':'D:/Data/MoS2/Phonon/D3BJ_FD_Efield/E0.025_D3BJ/band.yaml',
        '3.00 V/nm with vdw correction':'D:/Data/MoS2/Phonon/D3BJ_FD_Efield/E0.300_D3BJ_test1/band.yaml'}
Repository = [Data['Zero-field with vdw correction'],Data['0.25 V/nm with vdw correction'],
              Data['3.00 V/nm with vdw correction']]

label = list(Data.keys())
title = 'Phonon of bilayer MoS2'

# K_path
K_path = {'2D': [r'$\Gamma$', 'M', 'K', r'$\Gamma$'],
          '3D': [r'$\Gamma$','M', 'K', r'$\Gamma$', 'A', 'L', 'H', 'A']}

Kpoints = K_path['2D']  # Plotting the bands along 2D K_path

color = ['k','b','r']

#for i in range(len(Repository)):
    #a = GPD.VisualizePhononBand(Repository[i],Kpoints=Kpoints,color=color[i],label=label[i],ylim=[0,15],title=title)

#plt.legend(loc='upper left')

a = GPD.VisualizePhononBand(Repository[0],Kpoints=Kpoints,label_band='True',bands_labelled=[6, 9, 10, 11, 12],unit='cm-1',ylim=[0,500])

plt.show()

# print(legend)