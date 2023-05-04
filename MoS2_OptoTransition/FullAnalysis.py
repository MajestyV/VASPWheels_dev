import matplotlib.pyplot as plt
from VaspWheels import GetKpath,GetElectronicBands,Visualization,VisualizeBands

GE = GetElectronicBands.vasp()    # 调用GetElectronicBands模块（可以获取能带数据）
GK = GetKpath.vasp()              # 调用GetKpath模块（可以获取K点路径）

class full_analysis:
    ''' This class of function is designed for full analysis of electronic structure of target systems.  '''
    def __init__(self,EIGENVAL,DOSCAR,TDM,lattice,HSP_type):
        self.name = full_analysis

        # 存放晶体结构参数的字典
        lattice_dict = {'HEX': ['HEX', [3.16, 3.16, 12.9, 90, 90, 120], 'primitive'],
                        'ORT': ['ORT', [3.16, 5.47, 12.9, 90, 90, 90], 'unitcell']}
        lattice_param = lattice_dict[lattice]

        # 存放高对称点路径的字典
        HighSymPoint = {'HEX_2D': [r'$\Gamma$', 'M', 'K', r'$\Gamma$'],
                        'HEX_3D': [r'$\Gamma$', 'M', 'K', r'$\Gamma$', 'A', 'L', 'H', 'A'],
                        'ORT': [r'$\Gamma$', 'X', 'S', 'Y', r'$\Gamma$', 'S'],
                        'ORT_1': [r'$\Gamma$', 'Y', 'S', 'X', r'$\Gamma$', 'S'],
                        'ORT_2': [r'$\Gamma$', 'X', 'S', r'$\Gamma$', 'Y']}
        HSP_path = HighSymPoint[HSP_type]  # HSP - short for High Symmetry Point

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
        num_segments = len(HSP_path) - 1
        self.Kpath_projected, self.Knodes_projected = GK.ProjectKpath(self.Kpath, num_segments, LatticeCorrection='True',Lattice=lattice_param)

        # 从DOSCAR中提取态密度计算结果
        DOS_data = GE.GetData(DOSCAR,spin_polarized='False')  # 非自旋极化版本
        self.energy, self.DOS, self.TOS = [DOS_data['energy'], DOS_data['DOS'], DOS_data['integrated DOS']]

        # 从TDM中提取Transition Dipole Moment计算结果



    def GetBandgap(self): return self.Eg

    #def Plot_EnergyBands(self,):
        # 生成投影到一维的K点路径
        #num_segments = len(self.HSP_path) - 1
        #Kpath_projected, Knodes_projected = GK.ProjectKpath(self.Kpath, num_segments, LatticeCorrection='True', Lattice=self.lattice)

        #if shift_Fermi:  # 默认进行费米面调零
            #bands_shifted = GE.ShiftFermiSurface(self.bands, self.Ev_max)  # 费米面调零
            #VB.Electron_bands(Kpath_projected, bands_shifted, Knodes_projected, ylim=(-2, 5), y_major_tick=self.y_major, HighSymPoint=self.HSP_path, color=self.color)
        #else:
            #VB.Electron_bands(Kpath_projected, self.bands, Knodes_projected, ylim=(-2, 5), y_major_tick=self.y_major, HighSymPoint=self.HSP_path, color=self.color)


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
    data_directory = 'D:/Projects/OptoTransition/Data/MoS2_ElectronicStructure/Trilayer/E_prop_SYM'
    EIGENVAL = data_directory+'/EIGENVAL'
    DOSCAR = data_directory+'/DOSCAR'

    FA = full_analysis(EIGENVAL,DOSCAR,1,'HEX','HEX_2D')
    FA.Visualize()
