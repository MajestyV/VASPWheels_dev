import matplotlib.pyplot as plt
import VaspWheels as vw

if __name__=='__main__':
    # 指定数据文件总目录
    # Zhuhai

    # MMW502
    # 

    # 全局设定
    Fermi_factor = 0.20  # 费米面调零参数
    # Fermi_factor = 0.185

    num_segment = 3  # 能带分段数

    # 画图参数
    figsize = (4.5, 6)
    energy_range = (-5,5)
    dos_range = (0,30)

    # 提取态密度数据
    data_tdos = data_directory+'/dos/tot/TDOS.dat'
    data_Mo = data_directory+'/dos/Mo/PDOS_SUM.dat'
    data_S = data_directory+'/dos/S/PDOS_SUM.dat'

    x_dos, y_dos = vw.API_vaspkit.GetDOS(data_tdos,Fermi_adjust=Fermi_factor)
    x1_dos, y1_dos = vw.API_vaspkit.GetProjectedDOS(data_Mo, orbital='dx2-y2 pnm idxy',Fermi_adjust=Fermi_factor)  # Mo: dx2-y2 pnm idxy
    x2_dos, y2_dos = vw.API_vaspkit.GetProjectedDOS(data_Mo, orbital='dz2', Fermi_adjust=Fermi_factor)  # Mo: dz2
    x3_dos, y3_dos = vw.API_vaspkit.GetProjectedDOS(data_S, orbital='px pnm ipy', Fermi_adjust=Fermi_factor)  # S: px pnm ipy
    x4_dos, y4_dos = vw.API_vaspkit.GetProjectedDOS(data_S, orbital='pz', Fermi_adjust=Fermi_factor)  # S: pz

    # 提取能带数据
    bands_file = data_directory+'/bands/Mo/PBAND_SUM.dat'

    Kpath, Kpath_nodes = vw.API_vaspkit.GetProjectedKpath(bands_file, num_segment=num_segment)

    x_band, y_band = vw.API_vaspkit.GetBands(bands_file,Fermi_adjust=Fermi_factor)


    ####################################################################################################################
    # 画图模块
    # 设置坐标轴和网格配置
    fig = plt.figure(figsize=figsize)
    grid = plt.GridSpec(3, 4, hspace=0.2, wspace=0.1)

    # 设置刻度线方向
    plt.rcParams['xtick.direction'] = 'in'  # 将x轴的刻度线方向设置向内
    plt.rcParams['ytick.direction'] = 'in'  # 将y轴的刻度线方向设置向内
    # plt.tick_params(bottom=False, top=False, left=True, right=True)

    # main_plot = fig.add_subplot(grid[:-1, 1:])
    # subplot_x = fig.add_subplot(grid[-1, 1:], yticklabels=[], sharex=main_plot)
    # subplot_y = fig.add_subplot(grid[:-1, 0], xticklabels=[], sharey=main_plot)

    plot_bands = fig.add_subplot(grid[:-1, :3])
    # subplot_x = fig.add_subplot(grid[-1, :3], yticklabels=[], sharex=main_plot)
    plot_dos = fig.add_subplot(grid[:-1, 3], xticklabels=[], sharey=plot_bands)

    # 画图
    # plot_bands.plot(x_band, y_band, color=vw.colors.crayons['Navy Blue'])
    # plot_dos.plot(x_dos, y_dos, color=vw.colors.crayons['Navy Blue'])
    plot_bands.plot(x_band, y_band, color='k')
    plot_dos.plot(x_dos, y_dos, color='k')
    plot_dos.plot(x1_dos, y1_dos, color=VI.CMYK_to_RGB(75, 45, 0, 40))
    plot_dos.plot(x2_dos, y2_dos, color=VI.CMYK_to_RGB(0, 82, 88, 16))
    plot_dos.plot(x3_dos, y3_dos, color='#450D54')
    plot_dos.plot(x4_dos, y4_dos, color='#183E0C')

    # 能带图辅助分割线以及各种细节设置
    K_min, K_max = (min(Kpath), max(Kpath))  # 投影K空间路径的范围
    ymin, ymax = energy_range  # 从输入参数中读取要展示的能量范围

    # 画高对称点分割线
    for i in range(len(Kpath_nodes) - 2):  # 第一跟最后的一个高对称点跟能带图的左右边界重合，所以不必作分割线
        plot_bands.vlines(Kpath_nodes[i + 1], ymin, ymax, linewidth=1, linestyles='dashed', colors='k')

    # 画费米面分割线
    plot_bands.hlines(0, K_min, K_max, linewidth=1, linestyles='dashed', colors='k')
    plot_bands.set_xticks(Kpath_nodes, vw.HSP.HighSymPoint_2D['HEX'])  # 更换2D或者3D体系记得要改这里
    plot_bands.set_yticks([-5.0, -2.5, 0, 2.5, 5.0])
    plot_bands.set_xlim(K_min, K_max)
    plot_bands.set_ylim(ymin, ymax)

    plot_dos.set_xticks([])
    plot_dos.set_yticklabels([])
    dos_min, dos_max = dos_range  # 从输入参数中读取要展示的态密度范围
    plot_dos.hlines(0, dos_min, dos_max, linewidth=1, linestyles='dashed', colors='k')
    plot_dos.set_xlim(dos_min, dos_max)