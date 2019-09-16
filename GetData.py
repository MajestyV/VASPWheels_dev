import numpy as np
import re
from os import path

class geda:
    d = path.dirname(__file__)

    def __init__(self,DOSCAR=d+"/DOSCAR",bands=d+"/bands.out",kinput=d+"/kinput",pdos=d+"/total_dos.dat"):
        self.DOSCAR = DOSCAR
        self.bands = bands
        self.kinput = kinput
        self.pdos = pdos

    def GetEDOS(self,DataPath=""):
        if not DataPath:
            EDOS = self.DOSCAR
        else:
            EDOS = DataPath
        f = open(EDOS)
        line = f.readline()
        dos_list = []
        par_list = []
        i = 0
        while line:
            if i <= 4:
                i += 1
            else:
                if i == 5:
                    par = list(map(float, line.split()))
                    par_list.append(par)
                    i += 1
                else:
                    num = list(map(float, line.split()))
                    dos_list.append(num)
            line = f.readline()
        f.close()
        par_array = np.array(par_list)
        dos_array = np.array(dos_list)
        return dos_array

    def GetPDOS(self,DataPath=""):
        if not DataPath:
            PDOS = self.pdos
        else:
            PDOS = DataPath
        f = open(PDOS)
        line = f.readline()
        dos_list = []
        i = 0
        while line:
            g = re.search("# Sigma", line)
            if g:
                i += 1
            else:
                num = list(map(float, line.split()))
                dos_list.append(num)
            line = f.readline()
        f.close()
        dos_array = np.array(dos_list)
        return dos_array

    def GetBands(self,DataPath1="",DataPath2=""):
        if not DataPath1:
            Bands = self.bands
        else:
            Bands = DataPath1
        f1 = open(Bands)
        line = f1.readline()
        data_list = []
        i = 0
        while line:
            g = re.search("#gy*", line)
            if g:
                i += 1
            else:
                num = list(map(float, line.split()))
                data_list.append(num)
            line = f1.readline()
        f1.close()
        data_array = np.array(data_list)

        if not DataPath2:
            K = self.kinput
        else:
            K = DataPath2
        f2 = open(K)
        line = f2.readline()
        kpoints_list = []
        while line:
            data = line.split()
            k = [float(data[0]), float(data[1]), float(data[2])]
            kpoints_list.append(k)
            line = f2.readline()
        f2.close()
        kpoints = np.array(kpoints_list)
        nkpoints = len(kpoints_list)  # number of k-points

        nrows = data_array.shape[0]  # number of rows
        ncolumns = data_array.shape[1]  # number of columns
        nbands = ncolumns-1  # number of bands

        N = nkpoints-1
        Z = int((nrows-1)/(nkpoints-1))
        # Z = int(Z)
        a = 0
        x = []
        x.append(a)
        x1 = []
        for i in range(N):
            l = np.sqrt((kpoints[i+1,0]-kpoints[i,0])**2+(kpoints[i+1,1]-kpoints[i,1])**2+(kpoints[i+1,2]-kpoints[i,2])**2)
            s = l/Z
            for j in range(Z):
                a = a+s
                x.append(a)
            x1.append(a)

        return data_array,x1,nbands