import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import VaspWheels as vw

# 生成渐变色值的函数，详见：https://www.jb51.net/article/164617.htm
def gradual(rgb_start,rgb_stop,num_point=5,endpoint=True):
    r_0, g_0, b_0 = rgb_start
    r_1, g_1, b_1 = rgb_stop
    r, g, b = [np.linspace(r_0,r_1,num=num_point,endpoint=endpoint),
               np.linspace(g_0,g_1,num=num_point,endpoint=endpoint),
               np.linspace(b_0,b_1,num=num_point,endpoint=endpoint)]
    return r, g, b

# matplotlib数据保存
def SavingFigure(saving_directory,**kwargs):
    filename = kwargs['filename'] if 'filename' in kwargs else 'Untitled'  # 文件名
    format = kwargs['format'] if 'format' in kwargs else 'eps'  # 储存格式
    dpi = kwargs['dpi'] if 'dpi' in kwargs else 600  # 分辨率

    saving_address = saving_directory+'/'+filename+'.'+format  # 图像文件要储存到的绝对地址

    plt.savefig(saving_address, dpi=dpi, format=format)

    return


if __name__=='__main__':
    # data_directory = '/Users/liusongwei/OptoTransition/Data/Molecular_orbits/NoSYM/Data'
    data_directory = 'D:/PhD_research/OptoTransition/Data/Molecular_orbits/NoSYM/Data'

    E_field = ['0.00', '0.02', '0.04', '0.06']

    valence_tot, conduction_tot = [[],[]]
    for n in E_field:
        valence_data = data_directory+'/E'+n+'_Valence_Gamma.txt'
        conduction_data = data_directory+'/E'+n+'_Conduction_Lambda.txt'

        valence = pd.read_csv(valence_data, header=None, skiprows=[0,1,2,3], sep='\s+')
        conduction = pd.read_csv(conduction_data, header=None, skiprows=[0, 1, 2, 3], sep='\s+')

        valence_array = valence.values
        conduction_array = conduction.values
        # print(data_array)

        valence_tot.append(valence_array)
        conduction_tot.append(conduction_array)

    valence_tot, conduction_tot = (np.array(valence_tot),np.array(conduction_tot))

    # 画图模块
    index_ctrl = 3  # 控制序号

    # scaling_factor = 6.748342563230854  # e/Bohr^3 -> e/Angstrom^3
    scaling_factor = 3.571067672582813  # e/Bohr^2 -> e/Angstrom^2

    x_v, y_v = (valence_tot[index_ctrl,:,1],valence_tot[index_ctrl,:,0])
    x_c, y_c = (conduction_tot[index_ctrl,:,1],conduction_tot[index_ctrl,:,0])

    # 创建画布
    plt.figure(figsize=(1.5,4))

    # 设置刻度线方向
    plt.rcParams['xtick.direction'] = 'in'  # 将x轴的刻度线方向设置向内
    plt.rcParams['ytick.direction'] = 'in'  # 将y轴的刻度线方向设置向内

    plt.plot(x_v*scaling_factor,y_v,color=vw.ColorConvertion.CMYK_to_RGB(75, 45, 0, 40))
    plt.plot(x_c*scaling_factor,y_c,color=vw.ColorConvertion.CMYK_to_RGB(0, 82, 88, 16))

    plt.xlim(0,0.008)
    # plt.ylim(8.5248,42.2122)
    plt.ylim(6.9582,43.7788)

    plt.xticks([0,0.004,0.008])
    plt.yticks([])

    saving_directory = 'D:/PhD_research/OptoTransition/Data/Figures/Molecular_orbitals/LineProfile'
    SavingFigure(saving_directory, filename='E' + E_field[index_ctrl])
    SavingFigure(saving_directory,filename='E'+E_field[index_ctrl],format='png')  # For quick view

