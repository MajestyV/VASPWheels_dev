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

    def Visualize_band_n_dos(self,energy_range=(-3,5),dos_range=(0,15),shift_Fermi=True,figsize=(4.5,6)):
        if shift_Fermi:  # 默认进行费米面调零
            bands = GE.ShiftFermiSurface(self.bands, self.Ev_max)  # 对能带数据进行费米面调零
            energy = self.energy-self.Ev_max  # 对DOS数据进行费米面调零
        else:
            bands = self.bands
            energy = self.energy
        Kpath, Knodes = (self.Kpath_projected,self.Knodes_projected)  # 将实例变量的值赋予本地变量

        # 设置坐标轴和网格配置
        fig = plt.figure(figsize=figsize)
        grid = plt.GridSpec(3, 4, hspace=0.2, wspace=0.1)

        # 设置刻度线方向
        plt.rcParams['xtick.direction'] = 'in'  # 将x轴的刻度线方向设置向内
        plt.rcParams['ytick.direction'] = 'in'  # 将y轴的刻度线方向设置向内
        #plt.tick_params(bottom=False, top=False, left=True, right=True)


        # main_plot = fig.add_subplot(grid[:-1, 1:])
        # subplot_x = fig.add_subplot(grid[-1, 1:], yticklabels=[], sharex=main_plot)
        # subplot_y = fig.add_subplot(grid[:-1, 0], xticklabels=[], sharey=main_plot)

        plot_bands = fig.add_subplot(grid[:-1, :3])
        # subplot_x = fig.add_subplot(grid[-1, :3], yticklabels=[], sharex=main_plot)
        plot_dos = fig.add_subplot(grid[:-1, 3], xticklabels=[], sharey=plot_bands)

        # 画图
        for i in range(self.num_bands):
            plot_bands.plot(Kpath,bands[i],color=vw.colors.crayons['Navy Blue'])
        plot_dos.plot(self.DOS,energy,color=vw.colors.crayons['Navy Blue'])

        # 能带图辅助分割线以及各种细节设置
        K_min, K_max = (min(Kpath), max(Kpath))  # 投影K空间路径的范围
        ymin, ymax = energy_range  # 从输入参数中读取要展示的能量范围

        print(Knodes)
        print(K_min, K_max)

        # 画高对称点分割线
        for i in range(len(Knodes) - 2):  # 第一跟最后的一个高对称点跟能带图的左右边界重合，所以不必作分割线
            plot_bands.vlines(Knodes[i + 1], ymin, ymax, linestyles='dashed', colors=vw.colors.crayons['Gray'])
        # 画费米面分割线
        plot_bands.hlines(0, K_min, K_max, linestyles='dashed', colors=vw.colors.crayons['Gray'])
        plot_bands.set_xticks(Knodes, self.HSP_path)
        plot_bands.set_xlim(K_min,K_max)
        plot_bands.set_ylim(ymin,ymax)

        plot_dos.set_xticks([])
        plot_dos.set_yticklabels([])
        dos_min, dos_max = dos_range  # 从输入参数中读取要展示的态密度范围
        plot_dos.set_xlim(dos_min,dos_max)

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
    structure = 'Bilayer'
    target_dir = 'E_prop_SYM'

    data_directory = main_dir+'/'+structure+'/'+target_dir

    EIGENVAL = data_directory+'/EIGENVAL'
    DOSCAR = data_directory+'/DOSCAR'

    FA = full_analysis(EIGENVAL,DOSCAR,1,'HEX','HEX',dimension='2D')
    FA.Visualize_band_n_dos(dos_range=(0,12.5))
    # 1-2 layer n bulk (0,12.5); 3-5 layer (0,30)

    saving_directory = 'D:/PhD_research/OptoTransition/Data/临时存放文件夹'  # Zhuhai
    vw.Save_Figure(saving_directory,structure)


