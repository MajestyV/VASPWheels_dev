import VaspWheels as vw

if __name__=='__main__':
    structure = 'Monolayer'

    # 指定数据文件总目录
    # Zhuhai

    # MMW502
    data_directory = 'D:/Projects/OptoTransition/Data/OrbitalAnalysis/'+structure+'/dos'  # MMW502

    # 保存目录
    saving_directory = 'D:/OneDrive/OneDrive - The Chinese University of Hong Kong/Desktop/DataFig_OptoTrans'  # MMW502
    # saving_directory = 'D:/Projects/OptoTransition/Data/Figures'  # JCPGH1

    saving_filename = structure+'_DOS'

    # 全局设定
    # Fermi_factor = 0.20  # 费米面调零参数
    Fermi_factor = 0.185

    # 画图参数

    # 提取态密度数据
    data_tdos = data_directory+'/total/TDOS_SOC.dat'
    data_Mo = data_directory+'/Mo/PDOS_SUM_SOC.dat'
    data_S = data_directory+'/S/PDOS_SUM_SOC.dat'

    x0_dos, y0_dos = vw.API_vaspkit.GetDOS(data_tdos,Fermi_adjust=Fermi_factor)
    x1_dos, y1_dos = vw.API_vaspkit.GetProjectedDOS(data_Mo, orbital='dx2-y2 pnm idxy',Fermi_adjust=Fermi_factor)  # Mo: dx2-y2 pnm idxy
    x2_dos, y2_dos = vw.API_vaspkit.GetProjectedDOS(data_Mo, orbital='dz2', Fermi_adjust=Fermi_factor)  # Mo: dz2
    x3_dos, y3_dos = vw.API_vaspkit.GetProjectedDOS(data_S, orbital='px pnm ipy', Fermi_adjust=Fermi_factor)  # S: px pnm ipy
    x4_dos, y4_dos = vw.API_vaspkit.GetProjectedDOS(data_S, orbital='pz', Fermi_adjust=Fermi_factor)  # S: pz

    x_dos = [x0_dos,x1_dos,x2_dos,x3_dos,x4_dos]
    y_dos = [y0_dos,y1_dos,y2_dos,y3_dos,y4_dos]

    color_list = ['#0A3B80','#5195F6','#F53526','#732BF5','#4AA82E']

    ####################################################################################################################
    # 画图模块
    vw.VisualElec_vaspkit.VisualizeDOS(x_dos,y_dos,mode='multiple',dos_range=(0,7),color_list=color_list)

    vw.SavingFigure(saving_directory=saving_directory, file_name=saving_filename)
    vw.SavingFigure(saving_directory=saving_directory, file_name=saving_filename, format='eps')