import cv2
import numpy as np
import matplotlib.pyplot as plt

class Gen_Nanoflake_Thinfilm:
    '''
    This package is designed to generate a 2D nanoflake thin-film using Monte Carlo method.
    在这个package中，我们通过随机多边形来表示二维纳米薄片，同时通过蒙特卡洛方法模拟纳米片通过溶液-凝胶法沉积到基底上形成薄膜的过程。
    '''
    def __init__(self,length=1000,width=1000,
                 nanoflake_size_range=(50,100),nanoflake_edges_range=(3,10),num_nanoflake=100):
        # self.name = Gen_Nanoflake_Thinfilm
        # 要可视化的薄膜区域大小，默认为10*10 μm^2的区域
        self.length = length
        self.width = width

        self.size_range = nanoflake_size_range  # 纳米片直径范围
        self.radius_range = (nanoflake_size_range[0]/2.0,nanoflake_size_range[1]/2.0)  # 纳米片半径范围
        self.edges_range = nanoflake_edges_range  # 纳米片的边数范围
        self.num_nanoflake = num_nanoflake  # 纳米片的数目

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
    # 纳米片生成模块
    # 此函数可以生成一系列可以用于构建随机多边形的点来构建纳米薄片 [generate points to construct a random nanoflake (polygon)]
    # num_edges (int): number of edges of the nanoflake
    # center (a list/tuple contain two numbers): coordinate of the center of the nanoflake
    # radius_range (a list/tuple containing two numbers): range of distances from center to polygon vertices
    # Returns: points (ndarray): points that can construct a random polygon
    def GenNanoflakes(self, num_edges, center, radius_range):
        angles = self.uniform_random(0, 2*np.pi, num_edges)
        angles = np.sort(angles)
        random_radius = self.uniform_random(radius_range[0], radius_range[1], num_edges)
        x = np.cos(angles) * random_radius
        y = np.sin(angles) * random_radius
        x = np.expand_dims(x, 1)
        y = np.expand_dims(y, 1)
        points = np.concatenate([x, y], axis=1)
        points += np.array(center)
        points = np.round(points).astype(np.int32)
        return points

    ####################################################################################################################
    # 可视化模块
    def ShowTopView(self, image_size, points, color):
        """
        draw polygon(s) on a image

        Parameters:
        -----------
        image_size: a list/tuple of numbers
            image size = [image_height, image_width, image_channel]
        points: 2D ndarray or a list of 2D ndarray
            points that can construct a random polygon, also can be a list of
            points that can construct random polygons
        color: a list/tuple of numbers, whose length is same as image channel
            color of polygon

        Returns:
        --------
        image: ndarray
            image with polygon(s) on it
        """
        image = np.zeros(image_size, dtype=np.uint8)
        if type(points) is np.ndarray and points.ndim == 2:
            image = cv2.fillPoly(image, [points], color)
        else:
            image = cv2.fillPoly(image, points, color)
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
    def GenThinfim(self):
        # nanoflake_coord = self.GenRandomCoordinate((0,self.length),(0,self.width),self.num_nanoflake)

        # 利用Numpy的random.randint来产生随机整数，随机生成纳米片边数
        num_edges = np.random.randint(self.edges_range[0], self.edges_range[1], size=self.num_nanoflake)
        # 生成一系列的随机坐标，以锚定纳米薄片的位置
        center = self.random_coordinate((0, self.length), (0, self.width), self.num_nanoflake)

        nanoflake_ensemble = []
        for i in range(self.num_nanoflake):
            nanoflake = self.GenNanoflakes(num_edges[i],center[i],self.radius_range)
            nanoflake_ensemble.append(nanoflake)

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
    GNT = Gen_Nanoflake_Thinfilm()

    a = GNT.GenRandomCoordinate((0,100),(0,100),200)

    print(a)
    plt.scatter(a[:,0],a[:,1])

