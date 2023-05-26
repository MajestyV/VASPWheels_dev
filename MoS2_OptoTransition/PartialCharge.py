import pandas as pd
import matplotlib.pyplot as plt

if __name__=='__main__':
    data_directory = '/Users/liusongwei/OptoTransition/Data/Molecular_orbits/NoSYM/Data'

    E_field = ['0.00', '0.02', '0.04', '0.06']

    for n in E_field:
        valence_data = data_directory+'/E'+n+'_Valence_Gamma.txt'
        conduction_data = data_directory+'/E'+n+'_Conduction_Lambda.txt'

        valence = pd.read_csv(valence_data, header=None, skiprows=[0,1,2,3], sep='\s+')
        conduction = pd.read_csv(conduction_data, header=None, skiprows=[0, 1, 2, 3], sep='\s+')

        valence_array = valence.values
        conduction_array = conduction.values
        # print(data_array)

        plt.plot(valence_array[:,1],valence_array[:,0],color = 'b')
        plt.plot(conduction_array[:,1],conduction_array[:,0],color = 'r')