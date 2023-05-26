# This script is designed to restore functions that could convert color data from one format to another.
# Enabled format: RGB, CMYK

import numpy as np

# 以下是颜色函数
# RGB值转换函数，可以将RGB值转换为matplotlib可读的归一化RGB值
def RGB(r,g,b): return np.array([r,g,b])/255.0  # 将RGB值归一化的函数，只有归一化的RGB值才能被matplotlib读取

# 此函数可以转换CMYK色值到归一化RGB色值
def CMYK_to_RGB(c, m, y, k, cmyk_scale=100, rgb_scale=255):
    r = rgb_scale * (1.0 - c / float(cmyk_scale)) * (1.0 - k / float(cmyk_scale))
    g = rgb_scale * (1.0 - m / float(cmyk_scale)) * (1.0 - k / float(cmyk_scale))
    b = rgb_scale * (1.0 - y / float(cmyk_scale)) * (1.0 - k / float(cmyk_scale))
    return np.array([r, g, b])/255.0