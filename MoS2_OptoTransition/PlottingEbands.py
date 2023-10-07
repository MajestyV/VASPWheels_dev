import VaspWheels as vw

if __name__=='__main__':
    # 要可视化的构型，同时也是保存文件名
    structure = 'Pentalayer'

    # 数据文件目录

    # Zhuhai
    # data_directory = 'D:/PhD_research/OptoTransition/Data/MoS2/Electronic_structure/Pentalayer/E_prop_SOC_SYM'
    # data_directory = 'D:/PhD_research/OptoTransition/Data/MoS2/Electronic_structure/Bulk/E_prop_SOC_SYM_MoreBands'

    # JCPGH1
    # data_directory = 'D:/Projects/OptoTransition/Data/MoS2_ElectronicStructure/Pentalayer/E_prop_SOC_SYM_9_9_1'
    # data_directory = 'D:/Projects/OptoTransition/Data/MoS2_ElectronicStructure/Pentalayer/E_prop_SOC_SYM_14_14_1'

    # MMW502
    # data_directory = 'D:/Projects/OptoTransition/Data/MoS2_ElectronicStructure/'+structure+'/E_prop_SOC_SYM'  # 1-4 层
    # data_directory = 'D:/Projects/OptoTransition/Data/MoS2_ElectronicStructure/' + structure + '/E_prop_SOC_SYM_MoreBands'  # 补充数据
    # data_directory = 'D:/Projects/OptoTransition/Data/MoS2_ElectronicStructure/'+structure+'/E_prop_SYM'  # Non SOC
    # data_directory = 'D:/Projects/OptoTransition/Data/MoS2_ElectronicStructure/Pentalayer/E_prop_SOC_SYM_14_14_1'  # Pentalayer
    # data_directory = 'D:/Projects/OptoTransition/Data/MoS2_ElectronicStructure/Bulk/E_prop_SOC_SYM'  # Bulk
    # data_directory = 'D:/PhD_research/Data/Simulation/MoS2/MoS2_pawpbe_vasp5_SOC/D3BJ/5/result'

    # Guangzhou
    data_directory = 'D:/PhD_research/OptoTransition/Data/MoS2_ElectronicStructure/Pentalayer/E_prop_SOC_SYM_14_14_1'  # Pentalayer - E = 0 V/nm
    # data_directory = 'D:/PhD_research/OptoTransition/Data/MoS2_ElectronicStructure/Pentalayer/Electric_field/E_0.10'  # Pentalayer - E = 1 V/nm

    # 保存目录
    # saving_directory = 'C:/Users/DELL/Desktop/DataFig_Desktop'  # Zhuhai
    # saving_directory = 'C:/Users/13682/OneDrive/桌面/Test'  # JCPGH1
    # saving_directory = 'D:/OneDrive/OneDrive - The Chinese University of Hong Kong/Desktop/DataFig_OptoTrans'  # MMW502
    saving_directory = 'C:/Users/DELL/Desktop/临时数据文件夹'  # Guangzhou

    EIGENVAL = data_directory+'/EIGENVAL'

    HighSymPath = vw.HighSymmetryPath._2D['HEX']  # 2D planar structure
    # HighSymPath = vw.HighSymmetryPath._3D['HEX']  # 3D bulk structure

    # 存放晶格常数的字典
    lattice_dict = {'HEX': ['HEX', [3.16, 3.16, 12.9, 90, 90, 120], 'primitive'],
                    'ORT': ['ORT', [3.16, 5.47, 12.9, 90, 90, 90], 'unitcell']}

    bands_data = vw.ElectronicStructure.GetEbands(EIGENVAL)  # 提取能带数据
    num_bands = bands_data['num_bands']                      # 能带总数
    num_kpoints = bands_data['num_kpoints']                  # K点总数
    Kpath = bands_data['Kpath']                              # K空间路径（三维）
    bands = bands_data['bands']                              # 能带具体的能量值

    Eg, Ev_max, Ec_min, extremum_location = vw.ElectronicStructure.GetBandgap(EIGENVAL, mode='occupation')

    print(Eg)

    # 画图模块
    num_segments = len(HighSymPath) - 1
    # 获取三维K空间路径在一维上的投影
    Kpath_projected, Knodes_projected = vw.ReciprocalSpace.ProjectKpath(Kpath, num_segments, lattice_param=lattice_dict['HEX'])

    bands_shifted = vw.ElectronicStructure.ShiftFermiSurface(bands,Ev_max)  # 费米面调零

    vw.VisualizeElectronic.VisualizeBands(Kpath_projected, bands_shifted,
                                          Knodes_projected, energy_range=(-4, 4), HighSymPath=HighSymPath, color=vw.colors.iColar['Paris'])

    vw.SavingFigure(saving_directory=saving_directory, file_name=structure)
    vw.SavingFigure(saving_directory=saving_directory, file_name=structure,format='eps')