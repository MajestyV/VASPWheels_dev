import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score

# 此函数可以利用pandas提取txt文件（也适用于dat文件）中的数据
# txt或dat文件中的数据形式应为两列式，第一列为自变量，第二列为因变量
def GetData_txt(data_file,**kwargs):
    header = kwargs['header'] if 'header' in kwargs else None  # 文件中的数据列，默认为没有列名，第一行作为数据读取
    sep = kwargs['sep'] if 'sep' in kwargs else '\s+'          # 数据分隔符，默认为'\s+'（指代\f\n\t\r\v这些）
    # 利用pandas提取数据，得到的结果为DataFrame格式
    data_DataFrame = pd.read_csv(data_file,header=header,sep=sep)  # 若header=None的话，则设置为没有列名
    data_array = data_DataFrame.values  # 将DataFrame格式的数据转换为数组
    x = data_array[:,0]  # 默认第一列为自变量
    y = data_array[:,1]  # 默认第二列为因变量
    return x,y


def GetData_csv(self, data_file, **kwargs):
    # 一些关于数据文件的参数
    header = kwargs['header'] if 'header' in kwargs else None  # 文件中的数据列，默认为没有列名，第一行作为数据读取
    x_col = kwargs['x_col'] if 'x_col' in kwargs else 0  # 默认第一列为自变量所在列
    y_col = kwargs['y_col'] if 'y_col' in kwargs else 1  # 默认第二列为因变量所在列

    # 利用pandas提取数据，得到的结果为DataFrame格式
    data_DataFrame = pd.read_csv(data_file, header=header)  # 若header=None的话，则设置为没有列名
    data_array = data_DataFrame.values  # 将DataFrame格式的数据转换为数组
    wavelength = data_array[:, x_col]  # 自变量所在列为波长
    intensity = data_array[:, y_col]  # 因变量所在列为强度

    return wavelength, intensity

# 多项式回归（Polynomial Regression）
# 此函数可利用多项式回归拟合测试结果
def PolynomialRegression(x,y,degree=2,reshaping='True'):
    if reshaping == 'True':   # 默认为不需要reshape
        x = x.reshape(-1, 1)  # sklearn的输入需要是二维数组
        y = y.reshape(-1, 1)  # 若输入为一维数组，则需reshape为二维数组才可以进行拟合，reshape很重要
    else:
        pass

    # 利用sklearn进行多项式回归拟合
    poly = PolynomialFeatures(degree=degree)  # 加入多项式函数特征
    poly.fit(x)
    x_poly = poly.transform(x)
    fitting_model = LinearRegression()  # 利用线性回归模块进行多项式回归
    fitting_model.fit(x_poly, y)

    fitting_result = fitting_model.coef_[0]  # 最后的拟合结果是二维数组，为方便后续运算及处理，我们将其转换为一维数组

    return fitting_result

# 此函数可以对输入的多项式系数进行展开，还原多项式回归的结果
# 自变量x可以是浮点数或者是一维数组，多项式回归的系数列表需要是一维数组
def Polynomial(x, coefficient):
    degree = len(coefficient)  # 多项式回归的阶数
    y_list = []
    for n in range(degree):
        y_list.append(coefficient[n]*x**n)  # 根据阶数，计算每一阶对函数总值的贡献
    y_mat = np.array(y_list)  # 将列表转换为二维数组，即矩阵
    y_total = y_mat.sum(axis=0)  # 进行每列的内部求和，即按列将整个矩阵求和成一行矩阵，结果为一维数组
    return y_total

###############################################################################################################
# 拟合结果分析模块
# 此函数可以对拟合结果进行分析，得到均方根误差跟决定因子
def Evaluate(y,y_fit,reshaping='false'):
    if reshaping == 'True':          # 默认为不需要reshape
        y = y.reshape(-1, 1)         # 将实际数据转换为二维数组
        y_fit = y_fit.reshape(-1,1)  # 将拟合结果转换为二维数组
    else:
        pass

    MSE = mean_squared_error(y, y_fit)  # Mean Squared Error (MSE)
    R2 = r2_score(y, y_fit)             # Coefficient of determination (R^2)

    # 拟合结果评估
    print(r'Mean Squared Error (MSE): %.5f' % MSE)
    print(r'Coefficient of Determination (R^2): %.5f' % R2)

    return MSE, R2

if __name__=='__main__':
    data_directory = 'D:/Projects/PhaseTransistor/Data/Simulation/CarrierTransport/4/Ort_supercell/Manual optimization/strain-energy profile/'

    filename = ['4_LocalMinimum_x_strain.dat','4_LocalMinimum_y_strain.dat']

    x1,y1 = GetData_txt(data_directory+filename[0],header=0)  # 设置header=0，则第一列会作为列名读取
    x2,y2 = GetData_txt(data_directory+filename[1],header=0)

    #parameter1 = PolynomialRegression(x1,y1)
    #parameter2 = PolynomialRegression(x2,y2)

    # print(x1)

    coef1 = np.polyfit(x1,y1,2)  # 对于简单的二次项回归这个会更加robust
    coef2 = np.polyfit(x2,y2,2)  # 对于简单的二次项回归这个会更加robust

    #print(parameter1,parameter2)
    print(-coef1[1]/(2*coef1[0]))
    print(-coef2[1]/(2*coef2[0]))
    print((0.01685448119947595+0.01952792991364153)/2)

    plt.scatter(x1,y1,color='b')
    plt.scatter(x2,y2,color='r')

    x = np.linspace(-0.1,0.1,100)
    plt.plot(x,np.polyval(coef1,x),color='b')
    plt.plot(x,np.polyval(coef2,x), color='r')

    plt.xlim(-0.065,0.065)
    plt.ylim(-174.5,-172.75)
