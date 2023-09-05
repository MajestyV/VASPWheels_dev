import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib import cm
from matplotlib.colors import ListedColormap, LinearSegmentedColormap
mpl.rcParams.update({'figure.dpi':150})

# 获取colormap: matplotlib.cm.get_cmap(name=None, lut=None)
# name：内置 colormap 的名称，如 'viridis'(默认)，'spring' 等
# lut：整数，重置 colormap 的采样间隔，默认是256
viridis = cm.get_cmap('viridis', 256)
jet = cm.get_cmap('jet', 256)
turbo = cm.get_cmap('turbo', 256)

print(turbo(0))