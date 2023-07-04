# 函数包的主体部分，导入专门用于处理VASP数据的函数脚本
from .API_for_VASP import ElectronicStructure  # 能带提取函数包
from .API_for_VASP import ReciprocalSpace      # K空间（倒易空间）相关函数包

# . 代表当前文件所在的文件夹路径（跟Linux shell script一样）
# 子package导入模块，方便外部调用
# 导入High symmetry point path数据
#from .HighSymmetryPath.HSP_path_2D import HighSymPoint_2D
#from .HighSymmetryPath.HSP_path_3D import HighSymPoint_3D
#from . import HighSymmetryPath as HSP
# 导入晶体学分析模块
from .Crystallography import Crystallography   # 晶体学相关计算函数包
from .Crystallography import HighSymmetryPath  # 高对称点路径


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