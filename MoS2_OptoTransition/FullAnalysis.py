import matplotlib.pyplot as plt
import VaspWheels as vw
from VaspWheels import GetKpath,GetElectronicBands,Visualization,VisualizeBands

GE = GetElectronicBands.vasp()    # 调用GetElectronicBands模块（可以获取能带数据）
GK = GetKpath.vasp()              # 调用GetKpath模块（可以获取K点路径）

class full_analysis:
    ''' This class of function is designed for full analysis of electronic structure of target systems.  '''
    def __init__(self,EIGENVAL,DOSCAR,TDM,lattice,HSP_type,dimension='3D'):
        self.name = full_analysis

        # 存放晶体结构参数的字典
        lattice_dict = {'HEX': ['HEX', [3.16, 3.16, 12.9, 90, 90, 120], 'primitive'],
                        'ORT': ['ORT', [3.16, 5.47, 12.9, 90, 90, 90], 'unitcell']}
        lattice_param = lattice_dict[lattice]

        # 从VaspWheels读取高对称点数据并存为字典，方便调用
        HighSymPoint = {'2D': vw.HSP.HighSymPoint_2D, '3D': vw.HSP.HighSymPoint_3D}
        self.HSP_path = HighSymPoint[dimension][HSP_type]  # HSP - short for High Symmetry Point

        # 数据提取模块
        # 从EIGENVAL中分析整理能带计算结果
        bands_dict = GE.GetEbands(EIGENVAL)  # 调用GetElectronicBands.vasp()中的函数提取能带计算数据
        self.num_bands = bands_dict['num_bands']  # 提取能带总数
        self.num_kpoints = bands_dict['num_kpoints']  # 提取K点总数
        self.Kpath = bands_dict['Kpath']  # K点路径
        self.bands = bands_dict['bands']  # 能带具体的能量值

        # 调用GetElectronicBands.vasp()中的函数对能带计算结果进行分析（寻找价带顶跟导带底以及计算带隙等）
        Eg, Ev_max, Ec_min, extremum_location = GE.GetBandgap(EIGENVAL, mode='occupation')
        self.Eg, self.Ev_max, self.Ec_min, self.extremum_location = [Eg, Ev_max, Ec_min, extremum_location]  # 转换为实例函数

        # 生成投影到一维的K点路径
        num_segments = len(self.HSP_path) - 1
        self.Kpath_projected, self.Knodes_projected = GK.ProjectKpath(self.Kpath, num_segments, LatticeCorrection='True',Lattice=lattice_param)
        # self.Kpath_projected = self.Kpath

        # 从DOSCAR中提取态密度计算结果
        DOS_data = GE.GetData(DOSCAR,spin_polarized='False')  # 非自旋极化版本
        self.energy, self.DOS, self.TOS = [DOS_data['energy'], DOS_data['DOS'], DOS_data['integrated DOS']]

        # 从TDM中提取Transition Dipole Moment计算结果



    def GetBandgap(self): return self.Eg



    def Visualize(self,shift_Fermi=True,figsize=(6,6)):
        if shift_Fermi:  # 默认进行费米面调零
            bands = GE.ShiftFermiSurface(self.bands, self.Ev_max)  # 对能带数据进行费米面调零
            energy = self.energy-self.Ev_max  # 对DOS数据进行费米面调零
        else:
            bands = self.bands
            energy = self.energy


        # 设置坐标轴和网格配置
        fig = plt.figure(figsize=figsize)
        grid = plt.GridSpec(4, 4, hspace=0.2, wspace=0.2)

        # main_plot = fig.add_subplot(grid[:-1, 1:])
        # subplot_x = fig.add_subplot(grid[-1, 1:], yticklabels=[], sharex=main_plot)
        # subplot_y = fig.add_subplot(grid[:-1, 0], xticklabels=[], sharey=main_plot)

        main_plot = fig.add_subplot(grid[:-1, :3])
        subplot_x = fig.add_subplot(grid[-1, :3], yticklabels=[], sharex=main_plot)
        subplot_y = fig.add_subplot(grid[:-1, 3], xticklabels=[], sharey=main_plot)

        # 画图
        for i in range(self.num_bands):
            main_plot.plot(self.Kpath_projected,bands[i],linewidth=0.5)
        subplot_y.plot(self.DOS,energy)

        main_plot.set_xlim(min(self.Kpath_projected),max(self.Kpath_projected))
        main_plot.set_ylim(-2,5)

        subplot_y.set_xlim(0,10)


# 正态分布数据的多子图显示

#mean = [0,0]
#cov = [[1,1], [1,2]]
#x, y = np.random.multivariate_normal(mean, cov, 3000).T



# 主轴坐标画散点图
#main_ax.plot(x, y, 'ok', markersize=3, alpha=0.2)

# 次轴坐标画直方图
#x_hist.hist(x, 40, histtype='stepfilled', orientation='vertical', color='red')
#x_hist.invert_yaxis()


#y_hist.hist(x, 40, histtype='stepfilled', orientation='horizontal', color='blue')
#x_hist.invert_xaxis()

if __name__=='__main__':
    # main_dir = 'D:/Projects/OptoTransition/Data/MoS2_ElectronicStructure/Trilayer/E_prop_SYM'  # MMW502
    # main_dir = 'D:/Projects/OptoTransition/Data/MoS2_ElectronicStructure/Bilayer/E_prop_SYM'  # JCPGH1
    main_dir = 'D:/PhD_research/OptoTransition/Data/MoS2/Electronic_structure'  # Zhuhai
    # structure = 'Bilayer'
    structure_list = ['Monolayer', 'Bilayer', 'Trilayer', 'Quadrilayer', 'Pentalayer', 'Bulk']
    # structure_list = ['Trilayer', 'Quadrilayer', 'Pentalayer']
    # structure_list = ['Bulk']
    target_dir = 'E_prop_SOC_SYM'

    dimension_list = ['2D', '2D', '2D', '2D', '2D', '3D']
    dos_range_list = [(0,12.5),(0,12.5),(0,30),(0,30),(0,30),(0,12.5)]

    for i in range(len(structure_list)):
        data_directory = main_dir+'/'+structure_list[i]+'/'+target_dir

        EIGENVAL = data_directory+'/EIGENVAL'
        DOSCAR = data_directory+'/DOSCAR'

        FA = full_analysis(EIGENVAL,DOSCAR,1,'HEX','HEX',dimension=dimension_list[i])
        FA.Visualize_band_n_dos(dos_range=dos_range_list[i])
        # 1-2 layer n bulk (0,12.5); 3-5 layer (0,30)

        saving_directory = 'D:/PhD_research/OptoTransition/Data/临时存放文件夹'  # Zhuhai
        vw.Save_Figure(saving_directory,structure_list[i])


