# 自定义色谱值
from .Custom_iColarmap import iColarmap

# 自定义色谱相关函数
# 基于matplotlib内置色谱创建新色谱模块
from .CustomizingColormap import GetColor_from_Colormap, InterceptMatplotlibColormap
# 自定义色谱创建模块
from .CustomizingColormap import CreateColormap, CreateSequentialColormap, CreateDivergingColormap, ShowColorbar