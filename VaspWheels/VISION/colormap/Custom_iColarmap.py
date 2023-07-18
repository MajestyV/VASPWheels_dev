# Customized colormap set designed for visualizing first-principles calculation results.
# Named by my love, Xiaolin Liu, created by Songwei Liu at 2023.07.17.

from .CustomizingColormap import CreateColormap, CreateDivergingColormap, CreateSequentialColormap  # 导入colormap生成函数

iColarmap = {
             'Coolwarm': CreateDivergingColormap('#265499','#DDDDDD','#B40426'),
             'Blue_n_Red': CreateDivergingColormap('#293485','#FFFFFF','#8C031E'),
             'Purple_n_Green': CreateDivergingColormap('#7202C2', '#FFFFFF', '#12290B'),
             'Brown_n_Green': CreateDivergingColormap('#422802', '#FFFFFF', '#051F18')
             }

color_range = ['#450D54', '#FFFFFF', '#183E0C']  # viridis_custom
# color_range = [VI.CMYK_to_RGB(75, 45, 0, 40), VI.CMYK_to_RGB(0, 0, 0, 0), VI.CMYK_to_RGB(0, 82, 88, 16)]  # coolwarm_custom  * 1.5