import cv2
import numpy as np
import matplotlib.pyplot as plt

class Gen_Nanoflake_Thinfilm:
    '''
    This package is designed to generate a 2D nanoflake thin-film using Monte Carlo method.
    在这个package中，我们通过随机多边形来表示二维纳米薄片，同时通过蒙特卡洛方法模拟纳米片通过溶液-凝胶法沉积到基底上形成薄膜的过程。
    单位：10 nm
    '''
    def __init__(self,length=1000,width=1000,
                 nanoflake_size_range=(50,200),nanoflake_edges_range=(3,10),num_nanoflake=100,threshold_area=0):
        # self.name = Gen_Nanoflake_Thinfilm
        # 要可视化的薄膜区域大小，默认为10*10 μm^2的区域
        self.length = length
        self.width = width

        self.size_range = nanoflake_size_range  # 纳米片直径范围
        self.radius_range = (nanoflake_size_range[0]/2.0,nanoflake_size_range[1]/2.0)  # 纳米片半径范围
        self.edges_range = nanoflake_edges_range  # 纳米片的边数范围
        self.num_nanoflake = num_nanoflake  # 纳米片的数目
        self.threshold_area = threshold_area  # 纳米片的面积阈值

        self.cm_data = [[0.2081, 0.1663, 0.5292], [0.2116238095, 0.1897809524, 0.5776761905],
 [0.212252381, 0.2137714286, 0.6269714286], [0.2081, 0.2386, 0.6770857143],
 [0.1959047619, 0.2644571429, 0.7279], [0.1707285714, 0.2919380952,
  0.779247619], [0.1252714286, 0.3242428571, 0.8302714286],
 [0.0591333333, 0.3598333333, 0.8683333333], [0.0116952381, 0.3875095238,
  0.8819571429], [0.0059571429, 0.4086142857, 0.8828428571],
 [0.0165142857, 0.4266, 0.8786333333], [0.032852381, 0.4430428571,
  0.8719571429], [0.0498142857, 0.4585714286, 0.8640571429],
 [0.0629333333, 0.4736904762, 0.8554380952], [0.0722666667, 0.4886666667,
  0.8467], [0.0779428571, 0.5039857143, 0.8383714286],
 [0.079347619, 0.5200238095, 0.8311809524], [0.0749428571, 0.5375428571,
  0.8262714286], [0.0640571429, 0.5569857143, 0.8239571429],
 [0.0487714286, 0.5772238095, 0.8228285714], [0.0343428571, 0.5965809524,
  0.819852381], [0.0265, 0.6137, 0.8135], [0.0238904762, 0.6286619048,
  0.8037619048], [0.0230904762, 0.6417857143, 0.7912666667],
 [0.0227714286, 0.6534857143, 0.7767571429], [0.0266619048, 0.6641952381,
  0.7607190476], [0.0383714286, 0.6742714286, 0.743552381],
 [0.0589714286, 0.6837571429, 0.7253857143],
 [0.0843, 0.6928333333, 0.7061666667], [0.1132952381, 0.7015, 0.6858571429],
 [0.1452714286, 0.7097571429, 0.6646285714], [0.1801333333, 0.7176571429,
  0.6424333333], [0.2178285714, 0.7250428571, 0.6192619048],
 [0.2586428571, 0.7317142857, 0.5954285714], [0.3021714286, 0.7376047619,
  0.5711857143], [0.3481666667, 0.7424333333, 0.5472666667],
 [0.3952571429, 0.7459, 0.5244428571], [0.4420095238, 0.7480809524,
  0.5033142857], [0.4871238095, 0.7490619048, 0.4839761905],
 [0.5300285714, 0.7491142857, 0.4661142857], [0.5708571429, 0.7485190476,
  0.4493904762], [0.609852381, 0.7473142857, 0.4336857143],
 [0.6473, 0.7456, 0.4188], [0.6834190476, 0.7434761905, 0.4044333333],
 [0.7184095238, 0.7411333333, 0.3904761905],
 [0.7524857143, 0.7384, 0.3768142857], [0.7858428571, 0.7355666667,
  0.3632714286], [0.8185047619, 0.7327333333, 0.3497904762],
 [0.8506571429, 0.7299, 0.3360285714], [0.8824333333, 0.7274333333, 0.3217],
 [0.9139333333, 0.7257857143, 0.3062761905], [0.9449571429, 0.7261142857,
  0.2886428571], [0.9738952381, 0.7313952381, 0.266647619],
 [0.9937714286, 0.7454571429, 0.240347619], [0.9990428571, 0.7653142857,
  0.2164142857], [0.9955333333, 0.7860571429, 0.196652381],
 [0.988, 0.8066, 0.1793666667], [0.9788571429, 0.8271428571, 0.1633142857],
 [0.9697, 0.8481380952, 0.147452381], [0.9625857143, 0.8705142857, 0.1309],
 [0.9588714286, 0.8949, 0.1132428571], [0.9598238095, 0.9218333333,
  0.0948380952], [0.9661, 0.9514428571, 0.0755333333],
 [0.9763, 0.9831, 0.0538]]

    ####################################################################################################################
    # 随机数生成模块

    # 此函数可以生成在区间[lower,upper)均匀分布的随机数（组），num指定了个数：1为单一随机数，大于1则为数目为num的随机数组
    def uniform_random(self,lower,upper,num=None): return (upper-lower)*np.random.random(num)+lower

    # 此函数可以生成一系列的随机坐标
    def random_coordinate(self, x_range, y_range, num):
        coordinate = np.zeros((num, 2), dtype=float)                         # 生成一个num行2列的二维数组存放数据
        coordinate[:, 0] = self.uniform_random(x_range[0], x_range[1], num)  # X轴坐标
        coordinate[:, 1] = self.uniform_random(y_range[0], y_range[1], num)  # Y轴坐标
        return coordinate

    ####################################################################################################################
    # 纳米片相关模块
    # 此函数可以生成一系列可以用于构建随机多边形的点来构建纳米薄片 [generate points to construct a random nanoflake (polygon)]
    # num_edges (int): number of edges of the nanoflake
    # center (a list/tuple contain two numbers): coordinate of the center of the nanoflake
    # radius_range (a list/tuple containing two numbers): range of distances from center to polygon vertices
    # Returns: points (ndarray): points that can construct a random polygon
    def GenNanoflakes(self, num_edges, center, radius_range):
        angles = self.uniform_random(0, 2*np.pi, num_edges)
        angles = np.sort(angles)
        # print(angles)
        # random_radius = self.uniform_random(radius_range[0], radius_range[1], num_edges)  # 不应该生成一系列radius，不然成不了凸包
        radius = self.uniform_random(radius_range[0], radius_range[1], 1)
        # print(radius)
        random_radius = np.array([radius[0] for i in range(num_edges)])
        x = np.cos(angles) * random_radius
        y = np.sin(angles) * random_radius
        x = np.expand_dims(x, 1)
        y = np.expand_dims(y, 1)
        points = np.concatenate([x, y], axis=1)
        points += np.array(center)
        points = np.round(points).astype(np.int32)
        return points

    # 此函数可以计算纳米片面积（参考：https://en.wikipedia.org/wiki/Shoelace_formula）
    def Area_Nanoflake(self,nanoflake):
        """
        compute polygon area
        polygon: list with shape [n, 2], n is the number of polygon points
        """
        area = 0
        q = nanoflake[-1]
        for p in nanoflake:
            area += p[0] * q[1] - p[1] * q[0]
            q = p
        return area/2.0

    ####################################################################################################################
    # 可视化模块
    # image_size (a list/tuple of numbers): image_size = [image_length, image_width, image_channel]
    # nanofalke_ensemble (2D ndarray or a list of 2D ndarray): point lists that could construct nanoflakes
    # color (a list/tuple of integer): color of the nanoflakes
    # Returns: image (ndarray): top view image of the nanoflake thinfilm
    def ShowTopView(self, image_size, nanoflake_ensemble, color):
        image = np.zeros(image_size, dtype=np.uint8)
        if type(nanoflake_ensemble) is np.ndarray and np.array(nanoflake_ensemble).ndim == 2:
            image = cv2.fillPoly(image, [nanoflake_ensemble], color)
        else:
            image = cv2.fillPoly(image, nanoflake_ensemble, color)
        return image

    ####################################################################################################################
    # 核心模块

    # 此函数可以随机生成一系列纳米片的参数
    #def GenNanoflakeParam(self):
        # 利用Numpy的random.randint来产生随机整数，随机生成纳米片边数
        #num_edges = np.random.randint(self.edges_range[0],self.edges_range[1],size=self.num_nanoflake)
        # 生成一系列的随机坐标，以锚定纳米薄片的位置
        #center = self.random_coordinate((0,self.length),(0,self.width),self.num_nanoflake)
        # 纳米片的尺寸
        # radius_range = self.uniform_random(self.radius_range[0], self.radius_range[1], self.num_nanoflake)  # 此行代码没有意义，随机再随机
        #return num_edges,center

    # 通过Monte Carlo方法，生成二维纳米片薄膜的俯视图（Top view）
    def GenThinfilm(self):
        # nanoflake_coord = self.GenRandomCoordinate((0,self.length),(0,self.width),self.num_nanoflake)

        # 利用Numpy的random.randint来产生随机整数，随机生成纳米片边数
        num_edges = np.random.randint(self.edges_range[0], self.edges_range[1], size=self.num_nanoflake)
        # 生成一系列的随机坐标，以锚定纳米薄片的位置
        center = self.random_coordinate((0, self.length), (0, self.width), self.num_nanoflake)

        image = np.zeros((self.length, self.width, 3), dtype=np.uint8)
        # 初始化循环
        i = 0
        nanoflake_ensemble = []
        while i < self.num_nanoflake:
            nanoflake = self.GenNanoflakes(num_edges[i],center[i],self.radius_range)
            # if self.Area_Nanoflake(nanoflake) >= self.threshold_area:
            if True:
                nanoflake_ensemble.append(nanoflake)
                image = cv2.fillPoly(image, nanoflake_ensemble, np.array(self.cm_data[i%63]) * 255)
                i +=1
            else:
                pass

            # nanoflake_ensemble.append(nanoflake)


        # image = self.ShowTopView((self.length, self.width, 3), nanoflake_ensemble, (255, 255, 255))

        cv2.imshow('b', image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

        # thinfilm_top_view =

        #points1 = random_polygon(10, [80, 80], [20, 50])
        #points2 = random_polygon(10, [80, 180], [20, 50])
        #points3 = random_polygon(3, [180, 80], [20, 50])
        #points4 = random_polygon(5, [180, 180], [20, 50])

        #pts = [points1, points2, points3, points4]

        # image1 = draw_polygon((256, 256, 3), points1, (255, 255, 255))
        #image2 = draw_polygon((256, 256, 3), pts, (255, 255, 255))
        # cv2.imshow('a', image1)
        #cv2.imshow('b', image2)
        #cv2.waitKey(0)
        #cv2.destroyAllWindows()

if __name__=='__main__':
    GNT = Gen_Nanoflake_Thinfilm(length=500,width=500,num_nanoflake=20)

    # a = GNT.GenRandomCoordinate((0,100),(0,100),200)
    GNT.GenThinfilm()

    #print(a)
    #plt.scatter(a[:,0],a[:,1])

