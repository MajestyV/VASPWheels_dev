import matplotlib.pyplot as plt
import VaspWheels as vw
from matplotlib import cm,colors

if __name__=='__main__':
    # SOC
    # Zhuhai
    data_file = 'D:/PhD_research/OptoTransition/Data/MoS2/Electronic_structure/OrbitalAnalysis/Bulk/Mo/PBAND_SUM_SOC.dat'

    # Non SOC
    # data_file = 'D:/Projects/OptoTransition/Data/MoS2_ElectronicStructure/Projected_bands/Bulk_SYM/bands/Mo/PBAND_SUM.dat'  # MMW502
    # data_file = 'D:/Projects/OptoTransition/Data/MoS2_ElectronicStructure/Projected_bands/Bulk_SYM/S/PBAND_SUM.dat'  # JCPGH1

    # 要分析的轨道
    orbital_list = ['dx2-y2 pnm idxy', 'dz2']  # Mo
    # orbital_list = ['px pnm ipy', 'pz']  # S

    # Fermi_factor = 0.20  # 费米面调零参数
    Fermi_factor = 0.185

    num_segments = 7

    Kpath, Kpath_nodes = vw.API_vaspkit.GetProjectedKpath(data_file, num_segment=num_segments)  # 获取K空间轨迹的一维投影

    # HighSymPath = vw.HighSymmetryPath._2D['HEX']  # 2D planar structure
    HighSymPath = vw.HighSymmetryPath._3D['HEX']  # 3D bulk structure

    # 获取能带数据
    x_band, y_band, w_band = vw.API_vaspkit.BiOrbitalAnalysis(data_file, orbital_list, Fermi_adjust=Fermi_factor)

    # 画图模块

    vw.VisualizeElectronic.VisualizeProjectedBands(x_band,y_band,w_band,Knodes_projected=Kpath_nodes,
                                                   colormap='seismic',
                                                   colormap_norm=(-1,1),HighSymPath=HighSymPath)