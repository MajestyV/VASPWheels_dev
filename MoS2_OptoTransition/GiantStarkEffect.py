import pandas as pd
import matplotlib.pyplot as plt
import VaspWheels as vw
from MoS2_OptoTransition import QuickVisual

#Q V = QuickVisual.QuickVisual(x_major=1.5, y_major=0.4)
# DR = QuickVisual.data_recording()

if __name__=='__main__':
    # JCPGH1
    # data_directory = 'D:/Projects/OptoTransition/Data/Stark_effect/Summary/5'  # Summary
    # data_directory = 'D:/Projects/OptoTransition/Data/Stark_effect/Bilayer/2_nonSOC_noSYM_FieldAllTheWay'  # Bilayer
    # data_directory = 'D:/Projects/OptoTransition/Data/Stark_effect/Pentalayer/5'  # Pentalayer

    # Guangzhou
    # data_directory = 'D:/PhD_research/OptoTransition/Data/MoS2_ElectronicStructure/Summary/E_prop_nonSOC_SYM'  # Band evolution
    data_directory = 'D:/PhD_research/OptoTransition/Data/Stark effect/Summary/5'  # Pentalayer

    # Band evolution
    # layer = ['1','2','3','4','5','Bulk']

    # General
    # E_field = ['0.25', '0.30', '0.35', '0.40', '0.45', '0.50']
    E_field = ['0.00','0.05','0.10','0.15','0.20','0.25','0.30','0.35','0.40','0.45','0.50']

    # Bilayer
    #E_field = ['0.000',
               #'0.025', '0.050', '0.075', '0.100', '0.125', '0.150', '0.175', '0.200', '0.225', '0.250','0.275',
               #'0.300', '0.325', '0.350', '0.375', '0.400', '0.425', '0.450', '0.475', '0.500', '0.525','0.550']
    # Pentalayer
    #E_field = ['0.00',
               #'0.01','0.02','0.03','0.04','0.05','0.06','0.07','0.08','0.09','0.10',
               #'0.11','0.12','0.13','0.14','0.15','0.16','0.17','0.18','0.19','0.20']
    #E_field = ['0.000',
    #'0.025', '0.050', '0.075', '0.100', '0.125', '0.150', '0.175', '0.200', '0.225', '0.250',
    #'0.275', '0.300', '0.325', '0.350', '0.375', '0.400', '0.425', '0.450', '0.475', '0.500']

    E_bandgap_total = []
    # for i in range(len(layer)): # Band evolution
    for i in range(len(E_field)): # Stark effect
        # data_file = data_directory + '/' + layer[i] + '/EIGENVAL'  # Band evolution
        data_file = data_directory+'/E_'+E_field[i]+'/EIGENVAL'  # Stark effect
        E_bandgap = vw.ElectronicStructure.GetBandgap(data_file)
        E_bandgap_total.append(E_bandgap[0])

    print(E_bandgap_total)

    ############################################分割线################################################

