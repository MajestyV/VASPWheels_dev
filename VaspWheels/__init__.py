import ElectronicStructure


# . 代表当前文件所在的文件夹路径（跟Linux shell script一样）
# 子package导入模块，方便外部调用
# 导入High symmetry point path数据
#from .HighSymmetryPath.HSP_path_2D import HighSymPoint_2D
#from .HighSymmetryPath.HSP_path_3D import HighSymPoint_3D
from . import HighSymmetryPath as HSP
# 导入画图色彩数据
#from .Gallery.colors.Seaborn_crayons import crayons
#from .Gallery.colors.Seaborn_xkcd import xkcd_rgb
from .Gallery import colors as colors  # 导入预设色值库
# 从colors中导入函数库
from .Gallery.colors import ColorConvertion as ColorConvertion  # 色值格式转换函数库

# 导入常用函数类
from .DataRecording import Save_Data, Save_Figure

# from VisualizeBands import plot_bands
# from GetElectronicBands import vasp

# 导入用于处理外部软件数据的API函数
from .API_for_external import API_vaspkit as API_vaspkit  # API for VASPKIT (https://vaspkit.com/)