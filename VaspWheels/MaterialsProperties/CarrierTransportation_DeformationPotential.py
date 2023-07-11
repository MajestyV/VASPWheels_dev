# 此代码专用于利用形变势理论研究材料的载流子传输
# This code is designed for investigating carrier transportation of materials via deformation potential theory.
# 参考文献详见：
# J. Bardeen and W. Shockley, Deformation Potentials and Mobilities in Non-Polar Crystals, Phys. Rev. 90, 72 (1950).
# Y. Cai, G. Zhang and Y.-W. Zhang, Polarity-Reversed Robust Carrier Mobility in Monolayer MoS2 Nanoribbons, J. Am. Chem. Soc. 136, 6269-6275 (2014).

import numpy as np
from scipy.optimize import leastsq
from VaspWheels import SI_unit as SI, UnitConversionFactor as unit_conv

##############################################################################################################
# 弹性模量计算模块（应变-能量分析），此函数可以通过分析strain-energy profile计算弹性模量
def ElasticModulus(strain,energy,structural_factor,dim='3D'):
    # 对于简单的二次项回归np.polyfit()函数会更加robust
    coef = np.polyfit(strain,energy,2)  # 多项式系数系数的排列从高到低，比如对于二次多项式，系数对于的次数依次为：2、1、0
    modulus = 2*coef[0]/structural_factor  # structural_factor随系统维数变化而变化：1D-长度，2D-面积，3D-体积

    # 量纲转换因子，转换过程为1D：eV/Å to N, 2D: eV/Å^2 to N/m, 3D: eV/Å^3 to N/m^2 = Pa （系统的维数默认为3D）
    unit_transform = {'1D': 1.602e-19/1.0e-10,
                      '2D': 1.602e-19/1.0e-20,
                      '3D': 1.602e-19/1.0e-30}
    return unit_transform[dim]*modulus

# Semiconductor conductivity calculation module (半导体导电性计算模块计算模块)

    # 能带载流子有效质量计算，详见：N. W. Ashcroft, N. D. Mermin. Solid State Physics, 1976: 213-239.
    # 以及面向维基科研：https://en.wikipedia.org/wiki/Effective_mass_(solid-state_physics)
    # 此函数可以计算在能带中运动的载流子的有效质量
    def CalculateEffectiveMass(self,Kstep,band,num_segment,**kwargs):
        num_point_total = len(band)  # 能带总点数
        num_point_segment = int(len(band)/num_segment)  # 每段能带中包含的点数
        # 每一段能带中，用于计算有效质量的点数，如不设置，则默认每段能带所有点都用于计算有效质量
        num_point_evaluating = kwargs['points_evaluating'] if 'points_evaluating' in kwargs else num_point_segment

        # 应注意，V.A.S.P.中计算能带默认的长度单位是Å，能量单位是eV，为将最后结果以电子静止质量m_{e}表示，我们需将输入数据转换为原子单位制
        # 在原子单位制中，长度单位为Bohr， 1 Bohr = 0.529177210903 Å, 1 Bohr^{-1} = 1.8897261246257702 Å^{-1}
        # 能量单位为Hartree， 1 eV = 0.0367493 Hartree
        Kstep = Kstep/1.8897261246257702  # K点路程中，每个点直接间隔的距离
        band = 0.0367493*np.array(band)

        Kpath_segment = np.array([i*Kstep for i in range(num_point_evaluating)])  # 生成衡量有效质量的能带的K空间路程点
        band_segmented = [band[i:i+num_point_evaluating] for i in range(0,num_point_total,num_point_segment)]  # 能带分段
        band_segmented_shifted = [np.array(band_segmented[i])-band_segmented[i][0] for i in range(num_segment)]  # 平移
        # print(band_segmented_shifted)

        # 接下来我们对运动在能带上的载流子的有效质量进行计算（https://yh-phys.github.io/2019/10/26/vasp-2d-mobility/）
        # 考虑到有效质量实际上就是能带曲率的倒数，我们先利用scipy的最小二乘法模块对能带进行二次项拟合，再对二次项的系数进行计算即可
        # 要利用scipy进行拟合，我们首先要定义两个函数
        # 由于我们把能带段起点平移到了原点开始，所以我们只需要考虑形如y=a*x^2的二次多项式，不需要考虑零次项跟一次项（二次多项式的极值点为原点）
        def polynomial(coefficient,x): return coefficient[0]*x**2
        def error(coefficient,x,y): return polynomial(coefficient,x)-y  # 拟合误差

        # scipy的最小二乘法拟合模块需要一个初猜值
        initial_guess = kwargs['initial_guess'] if 'initial_guess' in kwargs else np.array([0.5])
        EffectiveMass_list = []
        for i in range(num_segment):
            coef = leastsq(error, initial_guess, args=(Kpath_segment, band_segmented_shifted[i]))
            m_eff = 1.0/(2*coef[0][0])  # 计算有效质量
            EffectiveMass_list.append(m_eff)

        return EffectiveMass_list

    # 此函数可以基于载流子有效质量，计算导带亦或是价带的有效状态密度（Effective Density of States, Effective DOS）
    # S. M. Sze, K. K. Ng. Physics of Semiconductor Devices, 2006: 58-62.
    # E. F. Schubert. Physics Foundations of Solid-State Devices, 2006: chapter 12.
    # 为了方便配合上面的CalculateEffectiveMass()函数，输入的有效质量单位应为原子单位制，即以电子静止质量m_{e}表示
    # 同时输出的态密度单位为cm^-1，方便分析载流子浓度
    def EffectiveDOS(self,effective_mass,**kwargs):
        pi = np.pi  # 圆周率
        m_e = kwargs['electron_rest_mass'] if 'electron_rest_mass' in kwargs else self.m_e
        kB = kwargs['Boltzmann_constant'] if 'Boltzmann_constant' in kwargs else self.kB
        hbar = kwargs['reduced_Planck_constant'] if 'reduced_Planck_constant' in kwargs else self.hbar
        T = kwargs['temperature'] if 'temperature' in kwargs else 300.0  # 默认温度为300K

        # Number of equivalent energy minima (maxima) in conduction (valence) band
        # 详见：https://docs.quantumatk.com/tutorials/effective_mass/effective_mass.html
        M_c = kwargs['degeneracy_factor'] if 'degenracy_factor' in kwargs else 1.0
        m_eff = effective_mass * m_e  # 计算载流子有效质量

        dim = kwargs['dimension'] if 'dimension' in kwargs else '3D'
        EffectiveDOS_dict = {'0D': 2.0,
                             '1D': np.sqrt(m_eff*kB*T/(2.0*pi*hbar**2)),
                             '2D': m_eff*kB*T/(pi*hbar**2),
                             '3D': (1.0/np.sqrt(2))*(m_eff*kB*T/(pi*hbar**2))**(3.0/2.0)}


        scaling_dict =  {'0D':2.0, '1D': 1.0e-2, '2D': 1.0e-4, '3D': 1.0e-6}

        return M_c*EffectiveDOS_dict[dim]*scaling_dict[dim]

    # 通过玻尔兹曼统计，近似计算半导体的本征载流子浓度，详见：S. M. Sze, K. K. Ng. Physics of Semiconductor Devices, 2006: 16-21.
    def IntrinsicCarrierConcentration(self,band_gap,electron_effective_DOS,hole_effective_dos,**kwargs):
        kB = kwargs['Boltzmann_constant'] if 'Boltzmann_constant' in kwargs else self.kB
        T = kwargs['temperature'] if 'temperature' in kwargs else 300.0  # 默认温度为300K
        DOS_eff = np.sqrt(electron_effective_DOS*hole_effective_dos)
        return DOS_eff*np.exp(-band_gap/(2.0*kB*T))

    # 基于形变势理论（Deformation Theory）近似估算材料的载流子迁移率（J. Bardeen, W. Shockley. Phys. Rev. 80, 72 (1950).
    # Z. Shuai, et al.. Theory of Charge Transport in Carbon Electronic Materials, 2012: 67-73.
    def CarrierMobility(self,effective_mass,elastic_modulus,DP_constant,**kwargs):
        pi = np.pi  # 圆周率
        q = kwargs['elementary_charge'] if 'elementary_charge' in kwargs else self.q
        m_e = kwargs['electron_rest_mass'] if 'electron_rest_mass' in kwargs else self.m_e
        kB = kwargs['Boltzmann_constant'] if 'Boltzmann_constant' in kwargs else self.kB
        hbar = kwargs['reduced_Planck_constant'] if 'reduced_Planck_constant' in kwargs else self.hbar
        T = kwargs['temperature'] if 'temperature' in kwargs else 300.0  # 默认温度为300K

        m_eff = effective_mass * m_e  # 计算载流子有效质量
        # C = elastic_modulus*self.eV_to_J  # 弹性模量（又称为stiffness），默认输入的单位为eV/m，方便配合V.A.S.P.计算
        C = elastic_modulus  # 输入的单位为N/m
        E = DP_constant*self.eV_to_J  # 形变势常量（deformation potential constant），默认输入的单位为eV，方便配合V.A.S.P.计算
        print(E)

        dim = kwargs['dimension'] if 'dimension' in kwargs else '3D'
        mobility_dict = {'1D': q*C*(hbar**2)/(np.sqrt(2*pi*kB*T)*(m_eff**1.5)*(E**2)),
                         '2D': 2*q*C*(hbar**3)/((3.0*kB*T)*(m_eff**2.0)*(E**2)),
                         '3D': 2*np.sqrt(pi)*q*C*(hbar**4)/((3.0*(kB*T)**1.5)*(m_eff**2.5)*(E**2))}

        return mobility_dict[dim]*1e4

    # 此函数可以粗略地估算半导体电导率
    def Conductivity(self,n,p,electron_mobility,hole_mobility): return self.q*(n*electron_mobility+p*hole_mobility)
