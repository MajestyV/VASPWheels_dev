import matplotlib.pyplot as plt
from VaspWheels import GeneralAnalyzer,Visualization

GA = GeneralAnalyzer.functions()  #
VI = Visualization.plot()  # 调用Visualization模块

###################################################################################################################
# 数据

Efield = [0.125, 0.25, 0.375, 0.5, 0.625, 0.75, 0.875, 1.0]

me_K_l = [0.527487997,0.510721018,0.505257208,0.502294246,0.50028786,0.498763335,0.49752238,0.496454326]
me_K_t = [0.535576244,0.523794681,0.519838387,0.51762134,0.516065013,0.514855135,0.513847424,0.512964043]

mh_G_l = [-0.702649883,-0.734148725,-0.767670904,-0.799442475,-0.829174408,-0.857680371,-0.885577978,-0.913401315]
mh_G_t = [-0.702682975,-0.734184851,-0.767710405,-0.799485313,-0.829220492,-0.857729678,-0.885630545,-0.913493031]
# mh_G_l = [0.702649883,0.734148725,0.767670904,0.799442475,0.829174408,0.857680371,0.885577978,0.913401315]
# mh_G_t = [0.702682975,0.734184851,0.767710405,0.799485313,0.829220492,0.857729678,0.885630545,0.913493031]

###################################################################################################################
# 计算迁移率
DP_x_h, DP_x_e, DP_y_h, DP_y_e = [5.51686,6.42578,5.52182,6.99736]  # Deformation potential constant

modulus_x, modulus_y, modulus_x_modified, modulus_y_modified = [630.6813919,627.7555134,157.670348,156.9388784]

bulk_modulus_x, bulk_modulus_y = [242569766118.07947,241444428236.0711]

#u = GA.CarrierMobility(0.57,127.44,5.29,dimension='2D')
#print(u)
#u_e = GA.CarrierMobility(2.3*0.55,modulus_y_modified,DP_y_e,dimension='2D')
#u_h = GA.CarrierMobility(0.7026,modulus_y_modified,DP_y_h,dimension='2D')
u = GA.CarrierMobility(0.7026,bulk_modulus_y,DP_y_h)
print(u)
#print(u_e,u_h)


###################################################################################################################
# 画图模块

# Plotting effective mass
#VI.GlobalSetting(x_major_tick=0.2,y_major_tick=0.4)  # 全局设置

#blue = VI.MorandiColor('Paris')
#red = VI.MorandiColor('Redred')

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

# Plotting mobility
