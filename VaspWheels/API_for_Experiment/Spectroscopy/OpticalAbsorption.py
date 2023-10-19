# This code is designed to generate the Tauc plot based on the UV-vis absorption characterization data.
# J. Tauc, R. Grigorovici, A. Vancu. Phys. Stat. Sol., 15, 627 (1966).
# J. Tauc. Optical Properties of Solids, Abeles, North Holland, Amsterdam (1972).
# E. A. Davis, N. F. Mott. Philos. Mag., 22, 903 (1970).

import pandas as pd
import numpy as np
import scipy.stats as st

class Tauc_plot:
    def __init__(self):
        self.name = Tauc_plot
        # 一些常用的参数
        self.light_speed = 2.99792458e8  # [=] m/s
        self.Planck_constant = 4.136e-15  # [=] eV·s

    # 此函数可以对吸收光谱进行计算以生成Tauc所需的数据
    def Calculate(self,wavelength,absorbance,band_structure='direct'):
        wavelength, absorbance = [np.array(wavelength), np.array(absorbance)]  # 对输入数据进行转换，保证其为一维数组

        c = self.light_speed  # 引入全局参数
        h = self.Planck_constant

        if band_structure == 'direct':
            n = 1.0/2.0
        else:
            n = 2.0

        x = h*c/(wavelength*1e-9)  # 记得要将波长单位转换成m
        y = []
        for i in range(len(wavelength)):
            y.append((absorbance[i]*x[i])**(1.0/n))

        return np.array(x),np.array(y)

    # 此函数可以对Tauc plot进行选区线性拟合，输出的是拟合曲线的斜率与截距
    def LinearFit(self,data,fitting_area):  # 记住不要用range作为变量，不然会跟循环的range搞混，这种错误很难debug
        xmin, xmax = fitting_area  # 从范围中解压x轴的最大值跟最小值
        x_raw, y_raw = data  # 从data中解压x轴数据跟y轴数据

        x, y = [[], []]  # 创建两个空列表准备存放要拟合的数据
        for i in range(len(x_raw)):  # 截取要拟合的部分
            if x_raw[i] >= xmin and x_raw[i] < xmax:
                x.append(x_raw[i])
                y.append(y_raw[i])

        x = np.array(x)  # 转换为数组，方便拟合
        y = np.array(y)

        # 线性拟合，可以返回斜率，截距，r 值，p 值，标准误差
        slope, intercept, r, p, std_error = st.linregress(x,y)

        #print('$R^2$: '+r**2)  # 列印拟合结果分析
        #print('Standard error: '+std_error)

        return slope,intercept