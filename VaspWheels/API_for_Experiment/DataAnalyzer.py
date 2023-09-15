# This code is designed for providing useful functions in processing experimental data.

import numpy as np

########################################################################################################################
# 数据平滑处理模块（参考：https://blog.csdn.net/weixin_42782150/article/details/107176500）

# 滑动平均滤波，data应为一维数组，而windowsize应为整型
def Moving_average(data,windowsize,mode='same'):
    window = np.ones(int(windowsize))/float(windowsize)
    data_filtered = np.convolve(data, window, mode=mode)
    return data_filtered
