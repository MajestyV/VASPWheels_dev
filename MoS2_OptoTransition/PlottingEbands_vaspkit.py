import VaspWheels as vw

if __name__=='__main__':
    # SOC
    # Zhuhai
    # data_file = 'D:/PhD_research/OptoTransition/Data/MoS2/Electronic_structure/OrbitalAnalysis/Bulk/Mo/PBAND_SUM_SOC.dat'
    # MMW502
    # data_file = 'D:/Projects/OptoTransition/Data/OrbitalAnalysis/Bulk/S/PBAND_SUM_SOC.dat'
    # JCPGH1
    data_file = 'D:/Projects/OptoTransition/Data/OrbitalAnalysis/Monolayer/bands/BAND.dat'  # Monolayer
    # data_file = 'D:/Projects/OptoTransition/Data/OrbitalAnalysis/Bulk/S/PBAND_SUM_SOC.dat'  # Bulk

    # Non SOC
    # data_file = 'D:/Projects/OptoTransition/Data/MoS2_ElectronicStructure/Projected_bands/Bulk_SYM/bands/Mo/PBAND_SUM.dat'  # MMW502
    # data_file = 'D:/Projects/OptoTransition/Data/MoS2_ElectronicStructure/Projected_bands/Bulk_SYM/S/PBAND_SUM.dat'  # JCPGH1

    # 保存目录
    # saving_directory = 'D:\OneDrive\OneDrive - The Chinese University of Hong Kong\Desktop\DataFig_OptoTrans\OribitalAnalysis'  # MMW502
    saving_directory = 'D:/Projects/OptoTransition/Data/Figures'

    saving_filename = 'Monolayer'

    # Fermi_factor = 0.20  # 费米面调零参数
    Fermi_factor = 0.185

    num_segments = 3  # 2D
    # num_segments = 7  # 3D

    Kpath, Kpath_nodes = vw.API_vaspkit.GetProjectedKpath(data_file, num_segment=num_segments)  # 获取K空间轨迹的一维投影

    HighSymPath = vw.HighSymmetryPath._2D['HEX']  # 2D planar structure
    # HighSymPath = vw.HighSymmetryPath._3D['HEX']  # 3D bulk structure

    # 获取能带数据
    x_band, y_band = vw.API_vaspkit.GetBands(data_file,Fermi_adjust=Fermi_factor)

    # 画图模块
    vw.VisualElec_vaspkit.VisualizeBands(x_band,y_band,Knodes_projected=Kpath_nodes)

    vw.SavingFigure(saving_directory=saving_directory, file_name=saving_filename)
    vw.SavingFigure(saving_directory=saving_directory, file_name=saving_filename, format='eps')