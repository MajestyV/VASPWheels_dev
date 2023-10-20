# This code is designed for analyzing elemental distribution data gained from electron microscopic characterizations.
import numpy as np


class EDX:
    ''' This class of function is designed to analyze EDX data. '''
    def __init__(self,data,L,W,N,mode):
        self.L = L
        self.W = W
        self.N = N
        self.data = np.empty((L,W,N,2))

        # 检测模块，判断是点扫，线扫还是面扫

    def Intensity_to_AtomicPercentage(self):
        data_atomic_percentage = np.empty((self.L,self.W,self.N,1))
        for i in range(self.L):
            for j in range(self.W):
                for k in range(self.N):
                    elemental_sum = sum(self.data[i,j,k,])
                    data_atomic_percentage[i,j,k] =

