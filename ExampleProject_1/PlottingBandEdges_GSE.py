import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm,colors
from VaspWheels import GetElectronicBands,Visualization

GEB = GetElectronicBands.vasp()  #
VI = Visualization.plot()  #

aList = [1,2,3,4]
aList.reverse()
print(aList)

def MakeSchematic(band_edge):
    band_extracted_1 = list(band_edge[200:300])
    band_extracted_1.reverse()  # 将此段能带翻转
    band_extracted_2 = band_edge[270:299]
    band_extracted_3 = band_edge[201:220]
    return band_extracted_2+band_extracted_1+band_extracted_3

# data_directory = 'D:/PhD_research/Data/Simulation/MoS2/GSE/4/4_D3BJ_GSE_1_more_bands/'  # 宿舍电脑
data_directory = 'D:/Projects/PhaseTransistor/Data/Simulation/GSE/4/4_D3BJ_GSE_1_more_bands/'  # 办公室电脑

# Efield = ['0.000','0.025','0.050','0.075','0.100','0.125','0.150','0.175','0.200']
Efield = ['0.025','0.050','0.075','0.100','0.125','0.150','0.175','0.200']

#################################################################################################################
# 设置全局字体选项
font_config = {'font.family': 'Arial', 'font.weight': 'light'}  # font.family设定所有字体为font_type
plt.rcParams.update(font_config)  # 但是对于希腊字母(e.g. α, β, γ等)跟各种数学符号之类的不适用, Latex语法如Γ会被判断为None
# plt.rcParams['mathtext.default'] = 'regular'  # 可以通过这个选项修改所有希腊字母以及数学符号为Times New Roman

# 创建matplotlib的figure对象（figsize = (宽，高），单位为英寸；frameon可以控制要不要外边框）
fig = plt.figure(figsize=(32.0/15.0,1.6),frameon=False)

# 画示意图主图
main_fig = fig.add_axes([0.03,0.1,0.7,0.8])

plt.axis('off')  # 关掉所有外框线

x = range(0,148,1)

for i in range(len(Efield)):
    EIGENVAL = data_directory+'/'+Efield[i]+'/EIGENVAL'
    valence_band, conduction_band = GEB.GetBandEdges(EIGENVAL)  # 提取导带跟价带
    VB_schematic = MakeSchematic(valence_band)
    CB_schematic = MakeSchematic(conduction_band)

    Efermi = max(VB_schematic)
    VB_schematic, CB_schematic = [np.array(VB_schematic)-Efermi,np.array(CB_schematic)-Efermi]

    color = VI.CMYK_to_RGB(24+i*8,20+i*8,8+i*6,8)

    main_fig.plot(x,VB_schematic,color=color,linewidth=0.5)
    main_fig.plot(x,CB_schematic,color=color,linewidth=0.5)

sepline_color = VI.MorandiColor('Black')
plt.vlines(29,-1.45,2.4,linewidth=1,linestyles='dashed',color=sepline_color)
plt.vlines(80,-1.45,2.4,linewidth=1,linestyles='dashed',color=sepline_color)
plt.vlines(128,-1.45,2.4,linewidth=1,linestyles='dashed',color=sepline_color)
plt.text(26,-1.8,r'$\Gamma$',size=6)
plt.text(74,-1.8,r'$\Lambda_\mathrm{min}$',size=6)
plt.text(125,-1.8,'K',size=6)
plt.ylim(-1.7,2.2)

# 自定义colorbar
fig.subplots_adjust(right=0.8)
colorbar = fig.add_axes([0.8,0.12,0.04,0.78])

# print(VI.CMYK_to_RGB(30,20,8,8),VI.CMYK_to_RGB(80,70,48,8))  # RGB - [0.644  0.736  0.8464], [0.184  0.276  0.4784]
# print(VI.CMYK_to_RGB(24,14,6,8),VI.CMYK_to_RGB(80,70,48,8))  # RGB - [0.6992 0.7912 0.8648], [0.184  0.276  0.4784]
colors = [(0.6992,0.7912,0.8648),(0.184,0.276,0.4784)]
nbins = 100
cmap_name = 'example'  # colormap名

cmap = cm.colors.LinearSegmentedColormap.from_list(cmap_name, colors, N=nbins)  # 创建 colormap
norm = cm.colors.Normalize(vmin=0.125, vmax=1.000)
# n_bin 越小，插值得到的颜色区间越少
cb = fig.colorbar(cm.ScalarMappable(cmap=cmap, norm=norm),cax=colorbar,orientation='vertical',
                    ticks=[0.125,0.250,0.375,0.500,0.625,0.750,0.875,1.000])
cb.outline.set_color('none')
cb.ax.set_title('Electric field (V/nm)',fontsize=6, pad = 5)
cb.ax.tick_params(which='major',direction='in',length=3,width=0.5,color='white',left=False,labelsize=6)

# 保存模块
saving_directory = 'D:/Projects/PhaseTransistor/Data/Figures/CarrierTransportation/Version_22.12.30/'  # 办公室电脑
VI.SavingFigure(saving_directory,filename='Band edge evolution',format='pdf')