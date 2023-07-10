# 此代码囊括了一系列的函数，以实现一系列功能，致力于为第一性原理研究中常见的数据分析与计算提供便利
# 高聚低耦，吾码所宗，以建理论，追本溯源

import numpy as np
import pandas as pd
from scipy.optimize import leastsq
from sklearn.metrics import mean_squared_error, r2_score

class functions:
    """ This class of functions is designed for general data analysis and computation in ab initio study. """
    def __init__(self):
        self.name = functions






    ##############################################################################################################
    # 数据拟合相关模块
    # 拟合结果分析函数，此函数可以对拟合结果进行分析，得到均方根误差跟决定因子
    def Evaluate(self, y, y_fit, reshaping='false'):
        # 将真实数据和拟合结果reshape为二维数组，方便sklearn包读取（不然会出错），默认为不需要reshape
        y, y_fit = [y.reshape(-1, 1),y_fit.reshape(-1, 1)] if reshaping == 'True' else [y,y_fit]
        # MSE-Mean Squared Error, R2-Coefficient of determination (R^2)
        MSE, R2 = [mean_squared_error(y, y_fit),r2_score(y, y_fit)]
        print(r'Mean Squared Error (MSE): %.5f'%MSE+r'; Coefficient of Determination (R^2): %.5f'%R2)  # 打印评估结果
        return MSE, R2

    ##############################################################################################################
    #########################################接下来的部分为特定功能的实现模块###########################################
    ##############################################################################################################





    ##############################################################################################################

    ##############################################################################################################
    # 未知领域