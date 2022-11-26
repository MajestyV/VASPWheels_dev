import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from matplotlib.pyplot import MultipleLocator
from VaspWheels import GetChargeDensity

GCD = GetChargeDensity.Charge()  # 调用GetChargeDensity模块

# 一些用于文章级结果图的matplotlib参数，由于这些参数都是通用的，所以可以作为全局变量设置
plt.rcParams['xtick.direction'] = 'in'  # 将x轴的刻度线方向设置向内
plt.rcParams['ytick.direction'] = 'in'  # 将y轴的刻度线方向设置向内
font_config = {'font.family':'Arial'}  # font.family设定所有字体为Times New Roman
plt.rcParams.update(font_config)  # 但是对于希腊字母(e.g. α, β, γ等)跟各种数学符号之类的不适用, Latex语法如$\Gamma$会被判断为None
plt.rcParams['mathtext.default'] = 'regular'  # 可以通过这个选项修改所有希腊字母以及数学符号为Times New Roman

# 数据地址
data_directory = "D:/Projects/PhaseTransistor/Data/Simulation/GSE/4/Differential_Charge_Density/more_bands/"  # 办公室电脑
CHGDIFF_1 = data_directory+'differential_charge_density_0.25 V-nm.vasp'
CHGDIFF_2 = data_directory+'differential_charge_density_0.50 V-nm.vasp'
CHGDIFF_3 = data_directory+'differential_charge_density_0.75 V-nm.vasp'
CHGDIFF_4 = data_directory+'differential_charge_density_1.00 V-nm.vasp'

# 提取数据
data_1 = GCD.ExtractCharge(CHGDIFF_1)
data_2 = GCD.ExtractCharge(CHGDIFF_2)
data_3 = GCD.ExtractCharge(CHGDIFF_3)
data_4 = GCD.ExtractCharge(CHGDIFF_4)

# 整理数据
charge_diff_2D_1 = GCD.Map_to_2D(data_1)
charge_diff_2D_2 = GCD.Map_to_2D(data_2)
charge_diff_2D_3 = GCD.Map_to_2D(data_3)
charge_diff_2D_4 = GCD.Map_to_2D(data_4)

####################################################################################################################
# 画图模块

# 创建matplotlib的figure对象
fig = plt.figure(figsize=(12,5),dpi=100,frameon=False)
# figsize = (宽，高），单位为英寸
# dpi是每平方英寸包含的像素
# frameon可以控制要不要外边框

# 为了等比例缩放实际图像，还原(110)晶面，我们需要得到构建这个晶面的坐标轴[1-10]跟[001]晶向的实际长度
# 经计算，|[1-10]| = 5.451335 A, 6*|[1-10]| = 32.70801 A, |[001]| = 43.91229 A
# 因此，我们可以设定我们的图例尺寸大致为宽*高 = 327*439
ratio = [0,327,-219.5,219.5]
# 因此，根据比例，5 A就相当于图例中的50个单位
# 所以我们可以以此来设置locator
#x_major_locator = MultipleLocator(50)  # 生成控制x轴刻度的locator
#y_major_locator = MultipleLocator(50)    # 生成控制y轴刻度的locator

#x_array = np.arange(0,327,50)          # 计算x轴刻度的数组，可以用以替换
#x_array_new = np.arange(0,3.207,0.5)        # 用以替换旧刻度的新刻度数组，记得要跟就数组一一对应（这种方法可以实现较为便捷的单位转换）
#y_array = np.array(list(np.arange(-200,-0.1,50))+list(np.arange(0,219.5,50)))  # 计算y轴刻度的数组，可以用以替换
#y_array_new = np.array(list(np.arange(-2,-0.1,0.5))+list(np.arange(0,2.3,0.5)))       # 用以替换旧刻度的新y轴刻度数组

# 在figure中添加第一幅子图，并将data_1数据可视化
axes_1 = fig.add_axes([0.03,0.2,0.2,0.6])        # 分配子图在figure中的位置
axes_1.set_title('$\mathcal{E}$ = 0.25 V/nm')          # 子图的标题
image_1 = axes_1.imshow(charge_diff_2D_1,extent=ratio,cmap='seismic',vmin=-6e-4,vmax=6e-4)
#axes_1.xaxis.set_major_locator(x_major_locator)  # 使用x轴locator
#axes_1.yaxis.set_major_locator(y_major_locator)  # 使用y轴locator
axes_1.set_xticks([])           # 通过这个函数，我们可以将旧的刻度(x_array)替换成新的刻度(x_array_new)
axes_1.set_yticks([])           # 记得要以数组的形式输入，同时数据的个数要一一对应
axes_1.set_xlabel(r'$[1\bar{1}0]$-direction (nm)')    # x轴名称
axes_1.set_ylabel(r'[001]-direction (nm)')                # y轴名称
#axes_1.set_xlabel(r'($\vec{a}$-$\vec{b}$)-direction (nm)')    # x轴名称
#axes_1.set_ylabel(r'$\vec{c}$-direction (nm)')                # y轴名称
#axes_1.set_xticks([])
#axes_1.set_yticks([])

# 在figure中添加第二幅子图，并将data_2数据可视化
axes_2 = fig.add_axes([0.25,0.2,0.2,0.6])        # 分配子图在figure中的位置
axes_2.set_title('$\mathcal{E}$ = 0.50 V/nm')          # 子图的标题
image_2 = axes_2.imshow(charge_diff_2D_2,extent=ratio,cmap='seismic',vmin=-6e-4,vmax=6e-4)
#axes_2.xaxis.set_major_locator(x_major_locator)  # 使用x轴locator
#axes_2.yaxis.set_major_locator(y_major_locator)  # 使用y轴locator
axes_2.set_xticks([])           # 通过这个函数，我们可以将旧的刻度(x_array)替换成新的刻度(x_array_new)
axes_2.set_yticks([])           # 记得要以数组的形式输入，同时数据的个数要一一对应
#axes_2.set_xlabel(r'($\vec{a}$-$\vec{b}$)-direction (nm)')    # x轴名称
#axes_2.set_ylabel(r'$\vec{c}$-direction (nm)')                # y轴名称
axes_2.set_xlabel(r'$[1\bar{1}0]$-direction (nm)')    # x轴名称

# 在figure中添加第三幅子图，并将data_3数据可视化
axes_3 = fig.add_axes([0.47,0.2,0.2,0.6])        # 分配子图在figure中的位置
axes_3.set_title('$\mathcal{E}$ = 0.75 V/nm')          # 子图的标题
image_3 = axes_3.imshow(charge_diff_2D_4,extent=ratio,cmap='seismic',vmin=-6e-4,vmax=6e-4)
#axes_3.xaxis.set_major_locator(x_major_locator)  # 使用x轴locator
#axes_3.yaxis.set_major_locator(y_major_locator)  # 使用y轴locator
axes_3.set_xticks([])           # 通过这个函数，我们可以将旧的刻度(x_array)替换成新的刻度(x_array_new)
axes_3.set_yticks([])           # 记得要以数组的形式输入，同时数据的个数要一一对应
axes_3.set_xlabel(r'$[1\bar{1}0]$-direction (nm)')    # x轴名称
#axes_3.set_ylabel(r'[001]-direction (nm)')                # y轴名称

# 在figure中添加第三幅子图，并将data_3数据可视化
axes_4 = fig.add_axes([0.69,0.2,0.2,0.6])        # 分配子图在figure中的位置
axes_4.set_title('$\mathcal{E}$ = 1.00 V/nm')          # 子图的标题
image_4 = axes_4.imshow(charge_diff_2D_4,extent=ratio,cmap='seismic',vmin=-6e-4,vmax=6e-4)
#axes_4.xaxis.set_major_locator(x_major_locator)  # 使用x轴locator
#axes_4.yaxis.set_major_locator(y_major_locator)  # 使用y轴locator
axes_4.set_xticks([])           # 通过这个函数，我们可以将旧的刻度(x_array)替换成新的刻度(x_array_new)
axes_4.set_yticks([])           # 记得要以数组的形式输入，同时数据的个数要一一对应
axes_4.set_xlabel(r'$[1\bar{1}0]$-direction (nm)')    # x轴名称
#axes_4.set_ylabel(r'[001]-direction (nm)')                # y轴名称

# 以子图的形式，添加colorbar，以第一幅子图的colorbar为基准，规范数据
axes_5 = fig.add_axes([0.93,0.25,0.01,0.5])

def fmt(x, pos):               # 此函数可以用于改变刻度
    return round(x*10000,2)

fig.colorbar(image_1,cax=axes_5,orientation='vertical',format=ticker.FuncFormatter(fmt))

axes_5.set_title(r'${\times}10^{-4}$ e/${\AA}^3$')  # matplotlib里面埃(Angstrom)的正确打法为: \AA
# 由于'\t'是转义字符，所以如果我们要打乘号'\times'，就在字符串前面加r，不然电脑会先识别成转义字符