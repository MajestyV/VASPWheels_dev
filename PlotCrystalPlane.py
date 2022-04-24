import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from matplotlib.pyplot import MultipleLocator

# 晶体坐标下，各轴的长度
lattice = np.array([[3.1473295667554400, 0.0000000000000000, 0.0000000000000000],
                    [-1.5736647833777198, 2.7256673589277995, 0.0000000000000000],
                    [0.0000000000000000, 0.0000000000000000, 43.9122903625234997]])

atomic_position_3D = np.array([[0.3333333429999996, 0.6666666870000029, 0.4310880238549544],    # Mo1
                               [0.3333333429999996, 0.6666666870000029, 0.7062630203979339],    # Mo2
                               [0.6666666269999979, 0.3333333129999971, 0.2937369796020661],    # Mo3
                               [0.6666666269999979, 0.3333333129999971, 0.5689119761450456],    # Mo4
                               [0.6666666870000029, 0.3333333429999996, 0.3954759305142161],    # S1
                               [0.6666666870000029, 0.3333333429999996, 0.6706304674638588],    # S2
                               [0.3333333129999971, 0.6666666269999979, 0.3293695325361412],    # S3
                               [0.3333333129999971, 0.6666666269999979, 0.6045240694857839],    # S4
                               [0.3333333129999971, 0.6666666269999979, 0.2580735384661423],    # S5
                               [0.3333333129999971, 0.6666666269999979, 0.5332994913558480],    # S6
                               [0.6666666870000029, 0.3333333429999996, 0.4667005086441520],    # S7
                               [0.6666666870000029, 0.3333333429999996, 0.7419264615338577]])    # S8

# 向量内积的定义： a·b可以理解为向量a在向量b上的投影再乘以b的长度|b|

# 由于原子坐标都在晶体坐标下，所以我们要先将原子坐标投影到(110)面再进行坐标轴长度的变换
x0 = np.array([1,-1,0])  # (110)面的x轴[1-10]晶向
y0 = np.array([0,0,1])   # (110)面的y轴[001]晶向

# 将原子往特定方向移动
def Shifting(coordinate,shifting_vec):
    coordinate = np.array(coordinate)
    shifting_vec = np.array(shifting_vec)
    return coordinate+shifting_vec

# 将3D坐标投影在由x-axis跟y-axis确定的特定平面上
def Projecting(coordinate,x_axis,y_axis):
    x_length = np.linalg.norm(x_axis,ord=2)
    y_length = np.linalg.norm(y_axis,ord=2)
    x = np.dot(coordinate,x_axis)/x_length
    y = np.dot(coordinate,y_axis)/y_length
    return [x,y]

atomic_position_3D_new = []
for i in range(12):
    atomic_position_3D_new.append(Shifting(atomic_position_3D[i],[0,-1,0]))

atomic_position_2D = []
for i in range(12):
    atomic_position_2D.append(Projecting(atomic_position_3D_new[i],x0,y0))

#print(atomic_position_2D)

for i in range(12):
    plt.scatter(atomic_position_2D[i][0],atomic_position_2D[i][1])
plt.xlim(0,1.414)
plt.ylim(0,1)

# fig = plt.figure([])