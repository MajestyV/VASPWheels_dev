# 此函数包囊括了一系列的函数，以实现一系列功能，致力于为第一性原理研究中常见的数据分析与计算提供便利
# 高聚低耦，吾码所宗，以建理论，追本溯源

# 函数包的主体部分，导入专门用于处理VASP数据的函数脚本
from .API_for_VASP import AtomicStructure      # 原子结构构造与分析函数模块
from .API_for_VASP import ElectronicStructure  # 能带提取函数模块
from .API_for_VASP import ReciprocalSpace      # K空间（倒易空间）相关函数模块

# . 代表当前文件所在的文件夹路径（跟Linux shell script一样）
# 子package导入模块，方便外部调用
# 导入High symmetry point path数据
#from .HighSymmetryPath.HSP_path_2D import HighSymPoint_2D
#from .HighSymmetryPath.HSP_path_3D import HighSymPoint_3D
#from . import HighSymmetryPath as HSP
# 导入晶体学分析模块
from .Crystallography import Crystallography   # 晶体学相关计算函数包
from .Crystallography import HighSymmetryPath  # 高对称点路径

# 导入用于处理外部软件数据的API函数
from .API_for_external import API_vaspkit as API_vaspkit  # API for VASPKIT (https://vaspkit.com/)

# 导入画图模块
# 色彩模块
from .VISION import colors as colors                            # 导入预设色值库
from .VISION.colors import ColorConvertion as ColorConvertion   # 色值格式转换函数库
# 各种画图专用函数
from .VISION import Visualization as Visualization              # 核心画图模块
from .VISION import VisualizeBands as VisualizeBands            # 能带图可视化函数包

########################################################################################################################
# 接下来是一些通用模块的导入
# 这些函数或者字典形式储存的数据放置在VaspWheels的根目录下，通过__init__.py直接导入，方便外部调用
from .Foundation import SI_unit, UnitConversionFactor  # 导入常用的基本物理学常数
from .DataStorage import SavingData, SavingFigure      # 数据保存函数
