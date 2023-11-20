# High symmetry path (HSP) for two-dimensional (2D) materials
_2D = {'HEX':   [r'$\Gamma$', 'M', 'K', r'$\Gamma$'],
       'ORT':   [r'$\Gamma$', 'X', 'S', 'Y', r'$\Gamma$', 'S'],
       'ORT_1': [r'$\Gamma$', 'Y', 'S', 'X', r'$\Gamma$', 'S'],
       'ORT_2': [r'$\Gamma$', 'X', 'S', r'$\Gamma$', 'Y']}

# High symmetry path (HSP) for three-dimensional (3D) materials
_3D = {'HEX': [r'$\Gamma$', 'M', 'K', r'$\Gamma$', 'A', 'L', 'H', 'A']}

# 往3D的高对称路径中添加一些典型系统的高对称路径
_3D.update({'Ice_Ih': [r'$\Gamma$', 'M', 'K', r'$\Gamma$', 'A', 'L', 'H', 'A|L', 'M|K', 'H']})