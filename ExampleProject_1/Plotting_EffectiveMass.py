import matplotlib.pyplot as plt
from VaspWheels import Visualization

VI = Visualization.plot()  # 调用Visualization模块

###################################################################################################################
# 数据

Efield = [0.125, 0.25, 0.375, 0.5, 0.625, 0.75, 0.875, 1.0]

me_K_l = [0.527487997,0.510721018,0.505257208,0.502294246,0.50028786,0.498763335,0.49752238,0.496454326]
me_K_t = [0.535576244,0.523794681,0.519838387,0.51762134,0.516065013,0.514855135,0.513847424,0.512964043]

mh_G_l = [0.702649883,0.734148725,0.767670904,0.799442475,0.829174408,0.857680371,0.885577978,0.913401315]
mh_G_t = [0.702682975,0.734184851,0.767710405,0.799485313,0.829220492,0.857729678,0.885630545,0.913493031]

###################################################################################################################
# 画图模块

VI.GlobalSetting(x_major_tick=0.2,y_major_tick=0.2)  # 全局设置

blue = VI.MorandiColor('Paris')
red = VI.MorandiColor('Redred')

plt.plot(Efield, me_K_l, '^', markersize=7, color=blue,label=r'$\mathrm{m_e}$ at $K_l$')
plt.plot(Efield, me_K_t, 's', markersize=7, color=red,label=r'$\mathrm{m_e}$ at $K_t$')
plt.plot(Efield, mh_G_l, '^', markerfacecolor='none', markersize=7, color=blue,label=r'$\mathrm{m_h}$ at ${\Gamma}_l$')
plt.plot(Efield, mh_G_t, 's', markerfacecolor='none', markersize=7, color=red,label=r'$\mathrm{m_h}$ at ${\Gamma}_l$')

VI.FigureSetting(xlabel='Electric field (V/nm)', ylabel='Effective mass ($\mathrm{m_e}$)',
                 xlim=(0.025,1.1),ylim=(0.1,1.3),
                 legend='True')

plt.legend(loc='best')
