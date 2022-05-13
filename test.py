import numpy as np
import matplotlib.pyplot as plt
from VaspWheels import GetChargeDensity

GCD = GetChargeDensity.Charge()

# 数据地址
#CHGDIFF = 'D:/Projects/PhaseTransistor/Data/Simulation/GSE/4/Differential_Charge_Density/CHGDIFF-0.050.vasp'

# 提取数据
#data = GCD.ExtractCharge(CHGDIFF)

# v = GCD.Volume(data['lattice'])  # 计算原胞体积
# isosurface_level = 6.0e-4/v
# print(v)
print(1/0.529177210903)

# a = np.array([3.14733000000000, 0.00000000000000, 0.00000000000000])
# b = np.array([-1.57366500000000, 2.72566700000000, 0.00000000000000])
# c = np.array([0.00000000000000,0.00000000000000, 43.91229000000000])

# print(np.linalg.norm(6*(a-b),ord=2))
# print(np.linalg.norm(c,ord=2))