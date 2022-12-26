import matplotlib.pyplot as plt
import numpy as np
from matplotlib.ticker import MultipleLocator, FormatStrFormatter
from VaspWheels import GeneralAnalyzer,Visualization

GA = GeneralAnalyzer.functions()  #
VI = Visualization.plot()  # 调用Visualization模块

###################################################################################################################
# 数据
# 电场强度
Efield = [0.125, 0.25, 0.375, 0.5, 0.625, 0.75, 0.875, 1.0]
# 载流子有效质量
me_K_l = [0.527487997,0.510721018,0.505257208,0.502294246,0.50028786,0.498763335,0.49752238,0.496454326]
me_K_t = [0.535576244,0.523794681,0.519838387,0.51762134,0.516065013,0.514855135,0.513847424,0.512964043]

# mh_G_l = [-0.702649883,-0.734148725,-0.767670904,-0.799442475,-0.829174408,-0.857680371,-0.885577978,-0.913401315]
# mh_G_t = [-0.702682975,-0.734184851,-0.767710405,-0.799485313,-0.829220492,-0.857729678,-0.885630545,-0.913493031]
mh_G_l = [0.702649883,0.734148725,0.767670904,0.799442475,0.829174408,0.857680371,0.885577978,0.913401315]
mh_G_t = [0.702682975,0.734184851,0.767710405,0.799485313,0.829220492,0.857729678,0.885630545,0.913493031]
# 禁带宽度
Eg = [0.885102, 0.8191809999999999, 0.724844, 0.6132329999999997,
      0.4903400000000002, 0.354171, 0.20420900000000008, 0.05164800000000014]

###################################################################################################################
# 计算迁移率
DP_x_h, DP_x_e, DP_y_h, DP_y_e = [5.51686,6.42578,5.52182,6.99736]  # Deformation potential constant

modulus_x, modulus_y, modulus_x_modified, modulus_y_modified = [630.6813919,627.7555134,157.670348,156.9388784]

bulk_modulus_x, bulk_modulus_y = [242569766118.07947,241444428236.0711]

# 展示迁移率计算结果
#u = GA.CarrierMobility(0.57,127.44,5.29,dimension='2D')
#print(u)
#u_e = GA.CarrierMobility(2.3*0.55,modulus_y_modified,DP_y_e,dimension='2D')
#u_h = GA.CarrierMobility(0.7026,modulus_y_modified,DP_y_h,dimension='2D')
#u = GA.CarrierMobility(0.7026,bulk_modulus_y,DP_y_h)
#print(u)
#print(u_e,u_h)

###################################################################################################################
# 画图模块
# 通用设置
blue, red = [VI.MorandiColor('Paris'),VI.MorandiColor('Redred')]  # 常用色值

# 画载流子有效质量图（Plotting effective mass）
#VI.GlobalSetting(x_major_tick=0.2,y_major_tick=0.4)  # 全局设置

#plt.plot(Efield, mh_G_l, '>', markerfacecolor='none', markersize=7, color=blue,label=r'$m_h^*$ at ${\Gamma}_l$')
#plt.plot(Efield, mh_G_t, '<', markerfacecolor='none', markersize=7, color=red,label=r'$m_h^*$ at ${\Gamma}_t$')
#plt.plot(Efield, me_K_l, 's', markersize=7, color=blue,label=r'$m_e^*$ at $\mathrm{K}_l$')
#plt.plot(Efield, me_K_t, 'D', markersize=7, color=red,label=r'$m_e^*$ at $\mathrm{K}_t$')


#VI.FigureSetting(xlabel='Electric field (V/nm)', ylabel='Effective mass ($\mathrm{m_e}$)',
                 #xlim=(0.025,1.1),ylim=(-1.2,0.8),
                 #legend='True')

#plt.legend(loc='best',ncol=2,fontsize=16,frameon=False)

# saving_directory = 'D:/Projects/PhaseTransistor/Data/Figures/CarrierTransportation/'  # 办公室电脑
#saving_directory = 'D:/PhD_research/Figures/Carrier transportation/Effective mass/'  # 宿舍电脑
#VI.SavingFigure(saving_directory,filename='Effective mass',format='pdf')

# 画载流子迁移率图（Plotting mobility）

# 画迁移率，载流子浓度示意图
# 载流子迁移率简化关系
def mobility(electron_mass_eff,hole_mass_eff):
    electron_mass_eff,hole_mass_eff = [np.array(electron_mass_eff),np.array(hole_mass_eff)]  # 把输入转换为数组，以防出错
    return 1.0/abs(electron_mass_eff)**2+1.0/abs(hole_mass_eff)**2
# 载流子浓度简化关系
def concentration(band_gap):
    band_gap = np.array(band_gap)  # 把输入转换为数组，以防出错
    return np.exp(-band_gap/(2.0*0.025852))

#print(mobility(0.527487997,0.702649883))
#print(mobility(0.510721018,0.734148725))
#print(mobility(0.505257208,0.767670904))

# 一些全局设置
# 设置刻度线方向
plt.rcParams['xtick.direction'] = 'in'  # 将x轴的刻度线方向设置向内
plt.rcParams['ytick.direction'] = 'in'  # 将y轴的刻度线方向设置向内
# 设置全局字体选项
font_config = {'font.family': 'sans-serif'}  # font.family设定所有字体为Arial
plt.rcParams.update(font_config)  # 但是对于希腊字母(e.g. α, β, γ等)跟各种数学符号之类的不适用, Latex语法如Γ会被判断为None

fontsize = 16  # 字体大小

# 正式画图
fig = plt.figure()  # 创建matplotlib的fig对象
ax1 = fig.add_subplot(111)  # 增加子图ax1为主图

x_major_locator = MultipleLocator(0.2)  # 将x主刻度标签设置为x_major_tick的倍数
x_minor_locator = MultipleLocator(0.04)  # 将x主刻度标签设置为x_major_tick的倍数
y_major_locator = MultipleLocator(0.1)  # 将y主刻度标签设置为y_major_tick的倍数
y_minor_locator = MultipleLocator(0.02)  # 将y主刻度标签设置为y_major_tick/5.0的倍数
ax1.xaxis.set_major_locator(x_major_locator)
ax1.xaxis.set_minor_locator(x_minor_locator)
ax1.yaxis.set_major_locator(y_major_locator)
ax1.yaxis.set_minor_locator(y_minor_locator)

plt.tick_params(which='major', length=5)  # 设置主刻度长度
plt.tick_params(which='minor', length=2)  # 设置次刻度长度

ax1.plot(Efield, concentration(Eg), marker='o',markersize=7,color=blue,
                                    label=r'$n_{i} \propto exp(-\frac{E_g}{2k_{B}T})$')
ax1.set_ylim(-0.05,0.45)
ax1.set_xlabel('Electric field (V/nm)',fontsize=fontsize)
ax1.set_ylabel(r'Concentration ($(N_{c}N_{v})^{\frac{1}{2}}$)',fontsize=fontsize,color=blue)
# ax1.yaxis.set_ticks(labelsize=18)
ax1.tick_params(labelsize=fontsize,axis='x')
ax1.tick_params(labelsize=fontsize,axis='y',colors=blue)
ax1.tick_params(which='minor', colors=blue)  # 设置次刻度颜色

plt.legend(loc=(0.01,0.85),frameon=False,fontsize=fontsize)


ax2 = ax1.twinx()  # 在ax1中，增设第二纵轴，这个函数是画双坐标轴图的关键（this is the important function）

y_major_locator_r = MultipleLocator(0.25)  # 将y主刻度标签设置为y_major_tick的倍数
y_minor_locator_r = MultipleLocator(0.05)  # 将y主刻度标签设置为y_major_tick/5.0的倍数
ax2.yaxis.set_major_locator(y_major_locator_r)
ax2.yaxis.set_minor_locator(y_minor_locator_r)

ax2.plot(Efield, mobility(me_K_l,mh_G_l), marker='o', markersize=7,markerfacecolor='none',
                                          color=red,label=r'$\mu \propto \frac{1}{|m_e^*|}+\frac{1}{|m_h^*|}$')
ax2.set_ylim(4.875,6.125)
ax2.set_ylabel(r'Mobility ($2q\hbar^{2}C/3k_{B}T\mathrm{m_e}E_1^2$)',fontsize=fontsize,rotation=90,labelpad=22,color=red)
ax2.tick_params(labelsize=fontsize,colors=red)
ax2.tick_params(which='minor', colors=red)  # 设置次刻度颜色

# 由于画双轴，所以ax2会把ax1的一些设置覆盖，我们只需要改ax2的设置就好
ax2.spines['left'].set_color(blue)  # 设置左边框为蓝色
ax2.spines['right'].set_color(red)  # 设置右边框为红色

plt.legend(loc=(0.01,0.72),frameon=False,fontsize=fontsize)

plt.tight_layout()  # 防止画图时，图像分布失衡，部分文字显示被遮挡的情况

plt.show()