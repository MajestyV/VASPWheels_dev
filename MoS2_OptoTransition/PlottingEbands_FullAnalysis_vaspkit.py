import VaspWheels as vw

if __name__=='__main__':
    structure = 'Quadrilayer'

    # 指定数据文件总目录
    # Zhuhai

    # MMW502
    data_directory = 'D:/Projects/OptoTransition/Data/OrbitalAnalysis/'+structure  # MMW502

    # 数据保存路径
    saving_directory = 'D:/OneDrive/OneDrive - The Chinese University of Hong Kong/Desktop/DataFig_OptoTrans'

    saving_filename = structure

    bands_file = data_directory+'/bands/total/BAND.dat'  # 能带计算结果文件地址
    dos_file = data_directory+'/dos/total/TDOS_SOC.dat'  # DOS计算结果文件地址

    Fermi_factor = 0.185  # 费米面调零参数
    # 能带分段数
    num_segments = 3  # 2D
    # num_segments = 7  # 3D
    # 高对称点路径
    HighSymPath = vw.HighSymmetryPath._2D['HEX']  # 2D planar structure
    # HighSymPath = vw.HighSymmetryPath._3D['HEX']  # 3D bulk structure


    Kpath, Kpath_nodes = vw.API_vaspkit.GetProjectedKpath(bands_file, num_segment=num_segments)  # 获取K空间轨迹的一维投影

    # 数据提取
    x_band, y_band = vw.API_vaspkit.GetBands(bands_file, Fermi_adjust=Fermi_factor)  # 提取能带数据
    x_dos, y_dos = vw.API_vaspkit.GetDOS(dos_file, Fermi_adjust=Fermi_factor)  # 提取DOS数据

    # 画图模块
    vw.VisualElectronic_vaspkit.FullAnalysis(x_band,y_band,Kpath_nodes,x_dos,y_dos,dos_range=(0,24),HighSymPath=HighSymPath)
    # dos_range=(0,28) for Pentalayer

    # 保存图像
    vw.SavingFigure(saving_directory=saving_directory, file_name=saving_filename)
    vw.SavingFigure(saving_directory=saving_directory, file_name=saving_filename, format='eps')