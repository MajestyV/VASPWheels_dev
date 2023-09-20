import numpy as np
import VaspWheels as vw
import matplotlib.pyplot as plt

def Rescale(data):
    data_rescaled = 10*(np.array(data)/(max(data)-min(data)))**2
    return data_rescaled

if __name__=='__main__':
    Efield = '0.00'
    # JCPGH1
    data_directory = 'D:/Projects/OptoTransition/Data/Homo-structure/Pentalayer/5_ProjectedBands_nonSOC_noSYM/E_'+Efield

    # MMW502
    # data_directory = 'D:/Projects/OptoTransition/Data/Homo-structure/Pentalayer/5_ProjectedBands_nonSOC_noSYM/E_'+Efield

    # Guangzhou
    # data_directory = 'D:/PhD_research/OptoTransition/Data/Homo-structure/Pentalayer/'+Efield+' V-nm'

    # layer_list = ['layer1', 'layer2', 'layer3', 'layer4', 'layer5']
    layer_list = ['layer5', 'layer4', 'layer3', 'layer2', 'layer1']
    # layer_list = ['Mo', 'S', 'Total']

    # 保存目录
    # saving_directory = 'D:/OneDrive/OneDrive - The Chinese University of Hong Kong/Desktop/DataFig_OptoTrans/OrbitalAnalysis'  # MMW502
    # saving_directory = 'D:/Projects/OptoTransition/Data/Figures/临时数据文件夹'  # JCPGH1

    # saving_filename = layer_list[control_index]

    # Fermi_factor = 0.20  # 费米面调零参数
    Fermi_factor = 0.195

    num_segments = 3  # 2D

    #Kpath, Kpath_nodes = vw.API_vaspkit.GetProjectedKpath(data_file, num_segment=num_segments)  # 获取K空间轨迹的一维投影
    #print(Kpath_nodes)

    K_range = [(1.8184,3.14956) for i in range(len(layer_list))]
    E_range = [(-2.2,2.2) for i in range(len(layer_list))]

    # 获取能带数据
    data = []
    for n in layer_list:
        data_file = data_directory + '/' + n + '/PBAND_SUM.dat'  # 数据地址
        # data_file = data_directory+'/Elementary/'+n+'/PBAND_SUM.dat'  # Test
        x_band, y_band, w_band = vw.API_vaspkit.GetProjectedBands(data_file, 'tot', Fermi_adjust=Fermi_factor)
        w_size = Rescale(w_band)
        data.append([x_band,y_band,w_band,w_size])

    # 画图模块
    # 色彩设定
    # cmap = vw.colormap.iColarmap['Coolwarm']
    # cmap = vw.colormap.iColarmap['Blue_n_Red']
    # cmap = vw.colormap.iColarmap['Purple_n_Green']
    # cmap = 'seismic'  # 采用matplotlib标准色谱
    # cmap = 'viridis'
    viridis_customed = vw.colormap.InterceptMatplotlibColormap('viridis',(30,100),100)
    print(vw.colormap.GetColor_from_Colormap(viridis_customed,[0,256],256))

    # 画能带图
    # jet_background = '#000080',
    # (data_series, num_data, subplot_location, subplot_shape, grid, K_range, **kwargs):

    #vw.Visualization_MultiPlot.Fatband_series(data,5,[[0,0],[0,1],[0,2],[0,3],[0,4]],
                                              #[[1,1],[1,1],[1,1],[1,1],[1,1]],(1,5),K_range,figsize=(16,4.2),
                                        #colormap_norm=(0,0.2),colormap=cmap)
    #vw.Visualization_MultiPlot.Plot_test(5,data,(1,5),
                                         #[[(0,0),(1,1)],[(0,1),(1,1)],[(0,2),(1,1)],[(0,3),(1,1)],[(0,4),(1,1)]],
                                         #K_range,figsize=(10,3.6),
                                         #colormap_norm=(0,0.2),colormap=cmap,color_background='#4E2271')
    #vw.Visualization_MultiPlot.VisualizeScatter_Fatband(len(layer_list), data, (1, 5),
                                         #[[(0, 0), (1, 1)], [(0, 1), (1, 1)], [(0, 2), (1, 1)], [(0, 3), (1, 1)],
                                          #[(0, 4), (1, 1)]],
                                         #y_major_tick=1,alpha=1.0,
                                         #figsize=(10, 3.6),xlim_list=K_range,ylim_list=E_range,
                                         #colormap=viridis_customed,color_background=np.array([0.253935,0.265254,0.529983]),colormap_norm=(0, 1.0))

    # 5层MoS2，每层对能带的贡献最多为1.0/5=0.2
    #vw.VisualElec_vaspkit.VisualizeProjectedBands(x_band,y_band,w_band,Knodes_projected=Kpath_nodes,
                                                  #colormap=cmap,size_band=np.abs(w_band)*4,
                                                  #y_major_tick=2,colormap_norm=(-1,1),HighSymPath=HighSymPath)

    saving_directory = 'D:/Projects/OptoTransition/Gallery/临时数据文件夹'  # JCPGH1
    # saving_directory = 'D:/Projects/OptoTransition/临时数据文件夹/Version_20230919'  # MMW502
    # saving_directory = 'D:/PhD_research/OptoTransition/Data/临时存放文件夹'  # Guangzhou
    saving_filename = 'QuantumWell_'+Efield
    #vw.SavingFigure(saving_directory=saving_directory, file_name=saving_filename)
    #vw.SavingFigure(saving_directory=saving_directory, file_name=saving_filename, format='eps')



    # 可视化并保存scalebar
    vw.CustomizingColormap.ShowColorbar(viridis_customed,(0,1))
    vw.SavingFigure(saving_directory=saving_directory, file_name=saving_filename+'_scalebar')
    vw.SavingFigure(saving_directory=saving_directory, file_name=saving_filename+'_scalebar', format='eps')