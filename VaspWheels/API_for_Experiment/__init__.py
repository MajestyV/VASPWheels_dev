# 直接声明函数，简化调用过程
# 滤波模块
from .DataFilter import Jumping_degree, Removing_jumping_point  # 跳变点去除模块
from .DataFilter import Moving_average  # 滑动平均滤波函数

# 调用子模块函数库
from .Spectroscopy import OpticalAbsorption  # 光谱学函数库
