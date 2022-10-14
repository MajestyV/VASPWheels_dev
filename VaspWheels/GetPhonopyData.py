import numpy as np
import yaml
import matplotlib.pyplot as plt

# 一些用于文章级结果图的matplotlib参数，由于这些参数都是通用的，所以可以作为全局变量设置
plt.rcParams['xtick.direction'] = 'in'  # 将x轴的刻度线方向设置向内
plt.rcParams['ytick.direction'] = 'in'  # 将y轴的刻度线方向设置向内
font_config = {'font.family':'Times New Roman'}  # font.family设定所有字体为Times New Roman
plt.rcParams.update(font_config)  # 但是对于希腊字母(e.g. α, β, γ等)跟各种数学符号之类的不适用, Latex语法如Γ会被判断为None
plt.rcParams['mathtext.default'] = 'regular'  # 可以通过这个选项修改所有希腊字母以及数学符号为Times New Roman

class Phonon:
    """ This class of function is written to extract and visualize V.A.S.P.+Phonopy calculation result. """

    def __init__(self):
        self.name = Phonon

    def ReadPhonopyData(self,band_yaml):
        with open(band_yaml) as f:
            data = yaml.load(f, Loader=yaml.FullLoader)
        return data

    def RearrangePhonopyData(self,PhonopyRawData,degree_of_freedom=3):
        nqpoint = PhonopyRawData['nqpoint']                         # Number of q-points calculated.
        npath = PhonopyRawData['npath']                             # Phonon calculation path in the reciprocal space
        segment_nqpoint = PhonopyRawData['segment_nqpoint']         # Number of q-points sampled along each path
        reciprocal_lattice = PhonopyRawData['reciprocal_lattice']   # Reciprocal lattice
        natom = PhonopyRawData['natom']                             # Number of atoms in the primitive cell.
        lattice = PhonopyRawData['lattice']                         # Crystal lattice information
        points = PhonopyRawData['points']                           # Atomic information
        phonon = PhonopyRawData['phonon']                           # Phonon data

        q_list = []
        q_projected = []
        nbands = natom*degree_of_freedom                            # Number of bands = Number of atoms * Degree of freedom
        frequency = np.zeros((nbands,nqpoint))
        for i in range(nqpoint):
            data = phonon[i]
            q_list.append(data['q-position'])
            q_projected.append(data['distance'])

            band = data['band']
            for j in range(nbands):
                frequency[j][i] = band[j]['frequency']

        return q_projected, frequency, nbands, nqpoint, npath

    def VisualizePhononBand(self,band_yaml,degree_of_freedom=3,**kwargs):
        raw_data = self.ReadPhonopyData(band_yaml)
        q_projected, frequency, nbands, nqpoint, npath = self.RearrangePhonopyData(raw_data,degree_of_freedom)

        # HSP - High Symmetry Point
        HSP_notation = kwargs['Kpoints'] if 'Kpoints' in kwargs else ['P' + str(n + 1) for n in range(npath+1)]
        HSP_position = [q_projected[0]]+[q_projected[int(nqpoint/npath)*i-1] for i in range(1,npath)]+[q_projected[len(q_projected)-1]]
        # 把初始点跟终点都包括进去

        xmin = q_projected[0]  # X轴范围
        xmax = q_projected[len(q_projected) - 1]
        ylim = kwargs['ylim'] if 'ylim' in kwargs else [0, 15]  # Y轴范围
        ymin, ymax = ylim
        color = kwargs['color'] if 'color' in kwargs else 'k'
        label = kwargs['label'] if 'label' in kwargs else None
        linewidth = kwargs['linewidth'] if 'linewidth' in kwargs else '0.6'

        label_band = kwargs['label_band'] if 'label_band' in kwargs else 'False'
        bands_labelled = kwargs['bands_labelled'] if 'bands_labelled' in kwargs else None
        labelling_color = kwargs['labelling_color'] if 'labelling_color' in kwargs else 'r'

        # 单位转换(太赫兹到波数)：1 THz= 33.35641 cm-1
        unit = kwargs['unit'] if 'unit' in kwargs else 'THz'
        if unit == 'cm-1':
            frequency = [[frequency[i][j]*33.35641 for j in range(len(frequency[i]))] for i in range(len(frequency))]
        else:
            pass

        for n in range(nbands):
            if label_band == 'True':
                if n+1 in bands_labelled:
                    #if bands_labelled.index(n+1) == 0:
                        #plt.plot(q_projected, frequency[n], linewidth=linewidth, color=labelling_color, label='Raman active')
                    #else:
                        #plt.plot(q_projected, frequency[n], linewidth=linewidth, color=labelling_color)
                    plt.plot(q_projected, frequency[n], linewidth=linewidth, color=labelling_color)
                else:
                    plt.plot(q_projected, frequency[n], linewidth=linewidth, color=color)
            else:
                if label and n==0:
                    plt.plot(q_projected,frequency[n],linewidth=linewidth,color=color,label=label)
                else:
                    plt.plot(q_projected,frequency[n],linewidth=linewidth,color=color)
        plt.xlim(xmin,xmax)
        plt.ylim(ymin,ymax)

        plt.vlines(HSP_position,ymin,ymax,linewidth=0.5,linestyles='dashed',colors='k')
        plt.hlines(0,xmin,xmax,linewidth=0.5,linestyles='dashed',colors='k')

        plt.xticks(HSP_position, HSP_notation, size=20)
        plt.yticks(size=14)

        if unit == 'cm-1':
            plt.ylabel('$\omega$ ($cm^{-1}$)', size=18)
        else:
            plt.ylabel('Frequency (THz)', size=18)

        if 'title' in kwargs:
            plt.title(kwargs['title'],size=26)
        else:
            pass

        return HSP_position, HSP_notation

# print(GetPhononBand(data_file))
# print(len(ReadPhonopyData(data_file)['phonon']))

if __name__=='__main__':
    #a = np.zeros((3,20))
    #print(a)
    #print(a[0])
    #print(a[2])

    data_file = 'D:/Data/MoS2/Phonon/D3BJ_IBRION6/test_vdw/band.yaml'

    phonon = Phonon()
    #a = phonon.ReadPhonopyData(data_file)
    #b = phonon.RearrangePhonopyData(a)
    Kpoints = [r'$\Gamma$', 'M', 'K', r'$\Gamma$']
    c = phonon.VisualizePhononBand(data_file,Kpoints=Kpoints)

    plt.show()

    print(c)
