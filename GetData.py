import numpy as np
import re
from os import path

class geda:
    d = path.dirname(__file__)

    def __init__(self,DOSCAR=d+"/DOSCAR",bands=d+"/bands.out",kinput=d+"/kinput",pdos=d+"/total_dos.dat",BindEner=d+"/binding-energy",POSCAR=d+"/POSCAR"):
        self.DOSCAR = DOSCAR
        self.bands = bands
        self.kinput = kinput
        self.pdos = pdos
        self.BindEner = BindEner
        self.POSCAR = POSCAR

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

    def GetBindingEnergy(self,DataPath=""):
        if not DataPath:
            bindener = self.BindEner
        else:
            bindener = DataPath
        f = open(bindener)
        line = f.readline()
        data_list = []
        Vol_list = []
        E_list = []
        i = 0
        while line:
            data =re.split('\s+', str(line))
            data_list.append(data)
            Vol_list.append(np.float(data[1]))
            E_list.append(np.float(data[4]))
            i += 1
            line = f.readline()
        f.close()
        Vol = np.array(Vol_list)
        E = np.array(E_list)
        return Vol,E,i

    def GetStructure(self,DataPath=""):
        if not DataPath:
            pos = self.POSCAR
        else:
            pos = DataPath
        f = open(pos)
        line = f.readline()
        lattice_list = []
        i = 0
        while line:
            if i <= 1:
                i += 1
            elif i <= 4:
                lv = list(map(float, line.split())) # lv = lattice vector
                lattice_list.append(lv)
                i += 1
            elif i == 6:
                na = np.float(line) # na = number of atoms in the unitcell
                i += 1
            else:
                i += 1
            line = f.readline()
        f.close
        lattice = np.array(lattice_list)
        return lattice,na