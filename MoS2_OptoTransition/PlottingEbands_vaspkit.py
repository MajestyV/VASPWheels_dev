import matplotlib.pyplot as plt
import VaspWheels as vw
from VaspWheels import Visualization

VI = Visualization.plot()  # 调用Visualization模块

if __name__=='__main__':
    # SOC


    # Non SOC
    data_file = 'D:/Projects/OptoTransition/Data/MoS2_ElectronicStructure/Projected_bands/Bulk_SYM/bands/Mo/PBAND_SUM.dat'  # MMW502
    # data_file = 'D:/Projects/OptoTransition/Data/MoS2_ElectronicStructure/Projected_bands/Bulk_SYM/S/PBAND_SUM.dat'  # JCPGH1

    # Fermi_factor = 0.20  # 费米面调零参数
    Fermi_factor = 0.185

    num_segment = 7  # 能带分段数

    Kpath, Kpath_nodes = vw.API_vaspkit.GetProjectedKpath(data_file, num_segment=num_segment)

    x_band, y_band = vw.API_vaspkit.GetBands(data_file, Fermi_adjust=Fermi_factor)

    # 画图模块
    # plt.rcParams['axes.facecolor'] = np.array([0,0,128])/255.0  # 更换背景颜色
    # 定义好各种参数，接下来是正式的画图部分
    VI.GlobalSetting(bottom_tick=False, y_major_tick=2.5)  # 引入画图全局变量

    plt.plot(x_band, y_band, color='k')

    plt.xlim(Kpath_nodes[0], Kpath_nodes[num_segment])
    plt.ylim(-5, 5)

    plt.hlines(0, Kpath_nodes[0], Kpath_nodes[num_segment], linewidth=1, linestyles='dashed', colors='k')
    for i in range(1, num_segment):
        plt.vlines(Kpath_nodes[i], -5, 5, linewidth=1, linestyles='dashed', colors='k')

