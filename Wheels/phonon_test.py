import numpy as np

class Dispersion():
    def __init__(self,DynamicalMatrix="",Kpoints=""):
        self.name = Dispersion
        if DynamicalMatrix:
            self.Dk = DynamicalMatrix
        if Kpoints:
            self.k = Kpoints

    def Phonon(self,DynamicalMatrix="",Kpoints="",n=200):
        if DynamicalMatrix:
            Dk = DynamicalMatrix
            k = Kpoints
        else:
            Dk = self.Dk
            k = self.k
        d = Dk.shape[0] # dimension
        nkpath = k.shape[0]-1 # number of K-path
        k_list = []
        l_list = []
        for i in range(nkpath):
            for j in range(n):




