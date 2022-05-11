import codecs
import re
import matplotlib.pyplot as plt
from VaspWheels import GetPhonopyData

GPD = GetPhonopyData.Phonon()  # 能带可视化专用包

Data = {'4_D3BJ_DFPT':'D:/Projects/PhaseTransistor/Data/Simulation/Phonon/4_D3BJ_DFPT/phonon/band.yaml',
        '4_D3BJ_FD_vdw':'D:/Projects/PhaseTransistor/Data/Simulation/Phonon/4_D3BJ_FD_vdw/phonon/band.yaml',
        '0.25 V/nm with vdw correction':'D:/Data/MoS2/Phonon/D3BJ_FD_Efield/E0.025_D3BJ/band.yaml',
        '3.00 V/nm with vdw correction':'D:/Data/MoS2/Phonon/D3BJ_FD_Efield/E0.300_D3BJ_test1/band.yaml'}
Repository = [Data['4_D3BJ_DFPT']]

label = list(Data.keys())
title = 'Phonon of quadrilayer MoS2'

# K_path
K_path = {'2D': [r'$\Gamma$', 'M', 'K', r'$\Gamma$'],
          '3D': [r'$\Gamma$','M', 'K', r'$\Gamma$', 'A', 'L', 'H', 'A']}

Kpoints = K_path['2D']  # Plotting the bands along 2D K_path

color = ['k','b','r']

#for i in range(len(Repository)):
    #a = GPD.VisualizePhononBand(Repository[i],Kpoints=Kpoints,color=color[i],label=label[i],ylim=[0,15],title=title)

#plt.legend(loc='upper left')

raman_active = [4, 5, 6, 9, 10, 12, 15, 16, 19, 20, 21, 22, 25, 26, 30, 32, 34, 36]
Eg = [4, 5, 9, 10, 15, 16, 19, 20, 21, 22, 25, 26]
A1g = [6, 12, 30, 32, 34, 36]

a = GPD.VisualizePhononBand(Repository[0],Kpoints=Kpoints,label_band='True',bands_labelled=raman_active,label='Raman active',unit='cm-1',ylim=[0,520],linewidth=1.2)

plt.legend(loc='upper left', frameon=False,fontsize=13)  # 由于迭代画图的关系，必须要在package加入这句话启用legend

plt.show()

# print(legend)