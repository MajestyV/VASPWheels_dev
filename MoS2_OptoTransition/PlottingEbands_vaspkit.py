import linecache  # Python标准库，内置的函数对于读取数据文件中特定行的内容等任务十分合适
import numpy as np
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
import VaspWheels as vw
from matplotlib import cm,colors
from VaspWheels import GetElectronicBands,GetKpath,Visualization

GE = GetElectronicBands.vasp()  # 调用GetElectronicBands模块
GK = GetKpath.vasp()  # 调用GetKpath模块
VI = Visualization.plot()  # 调用Visualization模块

if __name__=='__main__':
    # data_file = 'D:/Projects/OptoTransition/Data/MoS2_ElectronicStructure/Projected_bands/Pentalayer_SYM/S/PBAND_SUM.dat'  # MMW502
    data_file = 'D:/Projects/OptoTransition/Data/MoS2_ElectronicStructure/Projected_bands/Bulk_SYM/S/PBAND_SUM.dat'  # JCPGH1

    Fermi_factor = 0.185  # 费米面调零参数
    # Fermi_factor = 0

    num_segment = 7  # 能带分段数

    Kpath, Kpath_nodes = vw.API_vaspkit.GetProjectedKpath(data_file,num_segment=num_segment)
    print(Kpath)
    print(Kpath_nodes)

    # orbital_list = ['dx2-y2 pnm idxy', 'dz2']
    orbital_list = ['px pnm ipy','pz']

    x_band, y_band, w_band = vw.API_vaspkit.BiOrbitalAnalysis(data_file,orbital_list,Fermi_adjust=Fermi_factor)

    # 画图模块
    # plt.rcParams['axes.facecolor'] = np.array([0,0,128])/255.0  # 更换背景颜色
    # 定义好各种参数，接下来是正式的画图部分
    VI.GlobalSetting(bottom_tick=False, y_major_tick=2.5)  # 引入画图全局变量

    # cmap = 'bwr'
    # cmap = 'PRGn'

    # 热度图及colorbar的颜色设置
    color_range = ['#450D54', '#FFFFFF', '#183E0C']  # viridis_custom
    # color_range = [VI.CMYK_to_RGB(75, 45, 0, 40), VI.CMYK_to_RGB(0, 0, 0, 0), VI.CMYK_to_RGB(0, 82, 88, 16)]  # coolwarm_custom
    nbins = 100  # nbins越小，插值得到的颜色区间越少；反之，nbins越大，色谱越连续可分
    cmap_name = 'coolwarm_custom'  # colormap名
    cmap = cm.colors.LinearSegmentedColormap.from_list(cmap_name, color_range, N=nbins)  # 创建colormap

    cmap_norm = colors.Normalize(-1, 1)
    # 画投影能带
    # https://blog.shishiruqi.com//2019/05/19/pymatgen-band/
    # 用Matplotlib绘制渐变的彩色曲线：https://blog.csdn.net/xufive/article/details/127492212
    # 利用散点图实现渐变：https://www.brothereye.cn/python/427/
    plt.scatter(x_band, y_band, s=2, c=w_band, cmap=cmap, norm=cmap_norm)

    plt.xlim(Kpath_nodes[0],Kpath_nodes[num_segment])
    plt.ylim(-5,5)

    plt.hlines(0, Kpath_nodes[0],Kpath_nodes[num_segment], linewidth=1, linestyles='dashed', colors='k')
    for i in range(1,num_segment):
        plt.vlines(Kpath_nodes[i], -5, 5, linewidth=1, linestyles='dashed', colors='k')

    # 生成颜色条
    fig, ax = plt.subplots(figsize=(6, 1))
    fig.subplots_adjust(bottom=0.5)

    fig.colorbar(mpl.cm.ScalarMappable(cmap=cmap,norm=cmap_norm),cax=ax, orientation='horizontal', label='Weight')