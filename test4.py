import numpy as np

a1, a2, a3 = np.array([[1,2,0],[2,1,0],[3,0,1]])


a1_x_a2, a2_x_a3, a3_x_a1 = (np.cross(a1,a2),np.cross(a2,a3), np.cross(a3,a1))  # 提前算好基矢的交叉叉乘结果，方便调用以减少代码计算量

V = np.inner(a1,a2_x_a3)  # 计算实空间晶胞的体积

pi = np.pi
# reciprocal_lattice = (2.0*pi/V)*np.array([a2_x_a3,a3_x_a1,a1_x_a2])

reciprocal_lattice = (2.0*np.pi/V)*np.array([np.cross(a1,a2),np.cross(a2,a3), np.cross(a3,a1)])

# 倒空间基矢计算公式：b1 = 2*pi*(a2xa3)/[a1·(a2xa3)], b2 = 2*pi*(a3xa1)/[a1·(a2xa3)], b3 = 2*pi*(a1xa2)/[a1·(a2xa3)]
b1 = [(2.0*pi/V)*a2_x_a3[n] for n in range(len(a2_x_a3))]
b2 = [(2.0*pi/V)*a3_x_a1[n] for n in range(len(a3_x_a1))]
b3 = [(2.0*pi/V)*a1_x_a2[n] for n in range(len(a1_x_a2))]

print(np.array([b1,b2,b3]))
print(reciprocal_lattice)