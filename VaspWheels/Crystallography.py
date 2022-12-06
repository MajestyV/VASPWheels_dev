# This script is designed for crystallography analysis in aid of performing first-principle calculations.
# This code has referred to the article below when developing.
# W. Setyawan, S. Curtarolo. High-throughput electronic band structure calculations: Challenges and tools, Computational Materials Science, 49 (2010) 299-312.

import numpy as np

class Crystal:
    def __init__(self):
        self.name = Crystal

    # 简单的向量计算模块，所以向量都应该是三维的向量
    # 向量的点乘
    def dot_product(self,x,y):
        return np.array(x[0]*y[0]+x[1]*y[1]+x[2]*y[2])

    # 向量的叉乘
    def cross_product(self,x,y):
        product = [x[1]*y[2]-x[2]*y[1],
                   x[2]*y[0]-x[0]*y[2],
                   x[0]*y[1]-x[1]*y[0]]
        return np.array(product)

    # 计算不同晶格坐标中向量的模
    def length(self,vector,metric_tensor=np.array([[1.0,0,0],[0,1.0,0],[0,0,1.0]])):
        d_square = 0
        for i in range(len(vector)):
            for j in range(len(vector)):
                d_square = d_square+vector[i]*metric_tensor[i][j]*vector[j]
        d = np.sqrt(d_square)
        return d


    # There are 14 kinds of Bravais lattice within 7 kinds of lattice system. (7大晶系，14种布拉菲晶格）
    # Each lattice has its own set of lattice parameters, which is a list consisting with 6 parameters.
    # Typical lattice_parameter = [a, b, c, alpha, beta, gamma]
    # a, b, c is the three lattice constant, and alpha, beta, gamma is the three interaxial angle.
    # There are two types of lattice vectors: unitcell and primitive.
    # unitcell - The conventional lattice usually used in crystallography analysis.
    # primitive - The lattice consistent with the stoichiometry, used in first-principle calculations.
    def Bravais_lattice(self,lattice,lattice_parameter,lattice_type='primitive'):
        # 提取晶格常数
        a, b, c, alpha, beta, gamma = lattice_parameter

        # 构建unitcell的晶格向量
        unitcell_vectors = {'Orthorhombic': [[a,0,0],
                                             [0,b,0],
                                             [0,0,c]],
                            'Cubic': [[a,0,0],
                                      [0,a,0],
                                      [0,0,a]],
                            'Face-centered cubic': [[a,0,0],
                                                    [0,a,0],
                                                    [0,0,a]],
                            'Body-centered cubic': [[a,0,0],
                                                    [0,a,0],
                                                    [0,0,a]],
                            'Hexagonal': [[a/2.0, -a*np.sqrt(3)/2.0, 0],
                                          [a/2.0, a*np.sqrt(3)/2.0,0],
                                          [0,0,c]]}
        # 把缩写的选项也增加进去
        unitcell_abbreviate = {'ORT':unitcell_vectors['Orthorhombic'],
                               'CUB':unitcell_vectors['Cubic'],
                               'FCC':unitcell_vectors['Face-centered cubic'],
                               'BCC':unitcell_vectors['Body-centered cubic'],
                               'HEX':unitcell_vectors['Hexagonal']}
        unitcell_vectors.update(unitcell_abbreviate)

        # 构建primitive晶向
        primitive_vectors = {'Orthorhombic': [[0,b/2.0,c/2.0],
                                              [a/2.0,0,c/2.0],
                                              [a/2.0,b/2.0,0]],
                             'Cubic': [[a,0,0],
                                       [0,a,0],
                                       [0,0,a]],
                             'Face-centered cubic': [[0,a/2.0,a/2.0],
                                                     [a/2.0,0,a/2.0],
                                                     [a/2.0,a/2.0,0]],
                             'Body-centered cubic': [[-a/2.0,a/2.0,a/2.0],
                                                     [a/2.0,-a/2.0,a/2.0],
                                                     [a/2.0,a/2.0,-a/2.0]],
                             'Hexagonal': [[a, 0, 0],
                                           [-a/2.0, a*np.sqrt(3)/2.0, 0],
                                           [0, 0, c]]}
        # 同样，增加缩写
        primitve_abbreviate = {'ORT':primitive_vectors['Orthorhombic'],
                               'CUB':primitive_vectors['Cubic'],
                               'FCC':primitive_vectors['Face-centered cubic'],
                               'BCC':primitive_vectors['Body-centered cubic'],
                               'HEX':primitive_vectors['Hexagonal']}
        primitive_vectors.update(primitve_abbreviate)

        # 把两个字典分配到不同晶格的模式的键值之下
        lattice_vectors = {'unitcell': unitcell_vectors[lattice],
                           'primitive': primitive_vectors[lattice]}
        return lattice_vectors[lattice_type]

    # 计算实空间的度规张量(Metric Tensor)
    def MetricTensor(self,lattice,lattice_parameter,lattice_type='primitive'):
        a1, a2, a3 = self.Bravais_lattice(lattice,lattice_parameter,lattice_type)
        g = [[self.dot_product(a1,a1), self.dot_product(a1,a2), self.dot_product(a1,a3)],
             [self.dot_product(a2,a1), self.dot_product(a2,a2), self.dot_product(a2,a3)],
             [self.dot_product(a3,a1), self.dot_product(a3,a2), self.dot_product(a3,a3)]]
        return np.array(g)

    # 计算倒易空间基矢
    def Reciprocal_lattice(self,lattice,lattice_parameter,lattice_type='primitive'):
        # 计算正空间基矢
        a1, a2, a3 = self.Bravais_lattice(lattice,lattice_parameter,lattice_type)

        # 这实际上就是实空间晶胞的体积
        V = self.dot_product(a1,self.cross_product(a2,a3))

        # b1 = 2*pi*(a2xa3)/[a1·(a2xa3)], b2 = 2*pi*(a3xa1)/[a1·(a2xa3)], b3 = 2*pi*(a1xa2)/[a1·(a2xa3)]
        pi = np.pi
        b1 = [(2.0*pi/V)*self.cross_product(a2,a3)[n] for n in range(len(self.cross_product(a2,a3)))]
        b2 = [(2.0*pi/V)*self.cross_product(a3,a1)[n] for n in range(len(self.cross_product(a3,a1)))]
        b3 = [(2.0*pi/V)*self.cross_product(a1,a2)[n] for n in range(len(self.cross_product(a1,a2)))]

        return np.array([b1,b2,b3])

    # 计算倒易空间的度规张量
    def Reciprocal_MetricTensor(self,lattice,lattice_parameter,lattice_type='primitive'):
        b1, b2, b3 = self.Reciprocal_lattice(lattice,lattice_parameter,lattice_type)
        g_star = [[self.dot_product(b1,b1), self.dot_product(b1,b2), self.dot_product(b1,b3)],
                  [self.dot_product(b2,b1), self.dot_product(b2,b2), self.dot_product(b2,b3)],
                  [self.dot_product(b3,b1), self.dot_product(b3,b2), self.dot_product(b3,b3)]]
        return np.array(g_star)


    def Volume(self,lattice,lattice_parameter,lattice_type='primitive',space='real'):
        x, y, z = [None]*3
        if space == 'real':
            x, y, z = self.Bravais_lattice(lattice,lattice_parameter,lattice_type)
        elif space == 'reciprocal':
            x, y, z = self.Reciprocal_lattice(lattice,lattice_parameter,lattice_type)

        V = self.dot_product(x,self.cross_product(y,z))

        return V




if __name__ == '__main__':
    crystal = Crystal()
    #print(crystal.Bravais_lattice('FCC',[1,1,1,np.pi,np.pi,np.pi],'primitive'))
    #print(crystal.Reciprocal_lattice('FCC',[1,1,1,np.pi,np.pi,np.pi],'primitive'))
    #print(crystal.Volume('FCC',[1,1,1,np.pi,np.pi,np.pi],'unitcell'))
    #print(crystal.MetricTensor('Hexagonal',[2,2,5,90,90,120]))
    #print(crystal.Reciprocal_lattice('Hexagonal',[2,2,5,90,90,120]))
    metric = crystal.Reciprocal_MetricTensor('FCC',[1,1,1,90,90,90])
    print(metric)
    print(crystal.length([1/0.19,-0.85/0.19,0],metric))
    print(crystal.Volume('FCC',[1,1,1,90,90,90]))