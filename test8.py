import numpy as np

if __name__ == "__main__":
    x,y = (21,21)
    data = np.empty((x, y))
    for n in range(x):
        for m in range(y):
            data[n,m] = n*21+m+1  # 实际上要历遍一个21*21的网格，可以认为是在进行21进制的读数（indexing）
            # 第一列数据为测试波长所以要加一
