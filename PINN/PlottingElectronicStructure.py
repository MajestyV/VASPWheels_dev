import VaspWheels as vw

if __name__=='__main__':
    system_name = 'Ice_Ih'  # 目标系统名称

    # MMW502
    # data_file = 'D:/Projects/PINN_database/Ice_Ih/revPBE_D3/BAND.dat'  # data file
    # saving_directory = 'D:/Projects/PINN_database/Gallery'  # saving directory
    # Macbook
    data_file = '/Users/liusongwei/PINN_database/Ice_Ih/revPBE_D3/BAND.dat'
    saving_directory = '/Users/liusongwei/PINN_database/Gallery'
    # Non SOC
    # data_file = 'D:/Projects/OptoTransition/Data/MoS2_ElectronicStructure/Projected_bands/Bulk_SYM/bands/Mo/PBAND_SUM.dat'  # MMW502
    # data_file = 'D:/Projects/OptoTransition/Data/MoS2_ElectronicStructure/Projected_bands/Bulk_SYM/S/PBAND_SUM.dat'  # JCPGH1

    # 保存目录
    # saving_directory = 'D:/OneDrive/OneDrive - The Chinese University of Hong Kong/Desktop/DataFig_OptoTrans'  # MMW502

    # Fermi_factor = 0.20  # 费米面调零参数
    Fermi_factor = 0.91

    num_segments = 9  # 2D
    # num_segments = 7  # 3D

    Kpath, Kpath_nodes = vw.API_vaspkit.GetProjectedKpath(data_file, num_segment=num_segments)  # 获取K空间轨迹的一维投影
    print(Kpath_nodes)

    # HighSymPath = vw.HighSymmetryPath._2D['HEX']  # 2D planar structure
    HighSymPath = vw.HighSymmetryPath._3D['Ice_Ih']  # 3D bulk structure

    # 获取能带数据
    x_band, y_band = vw.API_vaspkit.GetBands(data_file, Fermi_adjust=Fermi_factor)

    # 画图模块
    vw.VisualElectronic_vaspkit.VisualizeBands(x_band, y_band,
                                               Knodes_projected=Kpath_nodes, HighSymPath=HighSymPath,
                                               energy_range=(-5, 10), y_major_tick=1.5)

    vw.SavingFigure(saving_directory=saving_directory, file_name=system_name)
    vw.SavingFigure(saving_directory=saving_directory, file_name=system_name, format='eps')