import VaspWheels as vw

if __name__=='__main__':
    # data_directory = 'D:/PhD_research/OptoTransition/Data/MoS2/Electronic_structure/Pentalayer/E_prop_SOC_SYM'
    data_directory = 'D:/Projects/OptoTransition/Data/MoS2_ElectronicStructure/Pentalayer/E_prop_SOC_SYM'

    EIGENVAL = data_directory+'/EIGENVAL'

    HighSymPath = vw.HighSymmetryPath._2D['HEX']

    # 存放晶格常数的字典
    lattice_dict = {'HEX': ['HEX', [3.16, 3.16, 12.9, 90, 90, 120], 'primitive'],
                    'ORT': ['ORT', [3.16, 5.47, 12.9, 90, 90, 90], 'unitcell']}

    bands_data = vw.ElectronicStructure.GetEbands(EIGENVAL)  # 提取能带数据
    num_bands = bands_data['num_bands']                      # 能带总数
    num_kpoints = bands_data['num_kpoints']                  # K点总数
    Kpath = bands_data['Kpath']                              # K空间路径（三维）
    bands = bands_data['bands']                              # 能带具体的能量值

    Eg, Ev_max, Ec_min, extremum_location = vw.ElectronicStructure.GetBandgap(EIGENVAL, mode='occupation')

    # 画图模块
    num_segments = len(HighSymPath) - 1
    # 获取三维K空间路径在一维上的投影
    Kpath_projected, Knodes_projected = vw.ReciprocalSpace.ProjectKpath(Kpath, num_segments, lattice_param=lattice_dict['HEX'])

    bands_shifted = vw.ElectronicStructure.ShiftFermiSurface(bands,Ev_max)  # 费米面调零

    vw.VisualizeBands.VisualizeElectronicBands(Kpath_projected, bands_shifted,
                                               Knodes_projected, ylim=(-2, 5), HighSymPath=HighSymPath)
    # VB.Electron_bands(Kpath_projected, bands_shifted, Knodes_projected, ylim=(-2, 5), HighSymPoint=HighSymPath)