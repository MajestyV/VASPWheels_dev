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

    def omega(self,nkpoints,nbands,frequency):
        w = np.zeros((nkpoints, nbands))
        for i in range(len(frequency)):
            m = i//nbands
            n = i%nbands
            for j in range(nbands):
                if n == j:
                    w[m,n] = frequency[i]
        return w

    def k_nomalizer(self,kpoints,npath,x,y,z):
        knodes = []
        nkpoints = len(kpoints)
        a = nkpoints/npath
        if nkpoints % npath == 0:
            for i in range(npath+1):
                if i == npath:
                    knodes.append(kpoints[nkpoints-1])
                else:
                    knodes.append(kpoints[i*a])
        else:
            for i in range(npath+1):
                knodes.append(kpoints[i*a])
        normalized_kpoints = []
        normalized_knodes = []
        normalized_knodes.append(0)
        for i in range(npath):
            l0 = np.sqrt(x**2*(knodes[i+1][0]-knodes[i][0])**2+y**2*(knodes[i+1][1]-knodes[i][1])**2+z**2*(knodes[i+1][2]-knodes[i][2])**2)
            dl = l0/np.float(a)
            normalized_knodes.append(normalized_knodes[i]+l0)
            for j in range(a):
                l = normalized_knodes[i]+j*dl
                normalized_kpoints.append(l)
                if (i == npath-1 and j == a-1) and nkpoints % npath != 0 :
                    normalized_kpoints.append(l+dl)
        return normalized_knodes,normalized_kpoints

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

    def GetElectronBands(self,DataPath1="",DataPath2=""):
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
            if i == 1:
                lattice_ratio = np.float(line)
            elif i>=2 and i <=4:
                lv = list(map(float, line.split()))  # lv = lattice vector
                lattice_list.append(lv)
            elif i == 6:
                na = np.float(line) # na = number of atoms in the unitcell (Modification in need to solve complex compounds.)
            i += 1
            line = f.readline()
        f.close
        lattice = np.array(lattice_list)
        return lattice,na,lattice_ratio

    def GetPhononBands(self,DataPath1="",x=1,y=1,z=1):
        #pattern = re.compile(r'^(-?d+)(.d+)?$')
        pattern1 = re.compile(r'\d+')
        pattern2 = re.compile(r'-?\d+\.?\d+')
        f = open(DataPath1)
        line = f.readline()
        kpoints = []
        frequency_list = []
        while line:
            if re.search("npath:",line):
                npath = pattern1.findall(line) # npath = number of k-paths
                npath = int(npath[0])
            elif re.search("natom:",line):
                natom = pattern1.findall(line) # natom = number of atoms
                natom = int(natom[0])
            elif re.search("- q-position:",line):
                k = pattern2.findall(line)
                k = map(float,k)
                kpoints.append(np.array(k))
            elif re.search("frequency:",line):
                frequency = pattern2.findall(line)
                frequency = float(frequency[0])
                frequency_list.append(frequency)
            line = f.readline()
        f.close()
        nkpoints = len(kpoints)

        nbands = 3*natom # nbands = number of bands
        w = self.omega(nkpoints,nbands,frequency_list)

        qnodes = self.k_nomalizer(kpoints,npath,x,y,z)[0]
        qpoints = self.k_nomalizer(kpoints,npath,x,y,z)[1]

        return qpoints,w,qnodes,nbands,nkpoints,npath

    def GetGruneisen(self,DataPath,x=1,y=1,z=1):
        pattern1 = re.compile(r'\d+')
        pattern2 = re.compile(r'-?\d+\.?\d+')
        f = open(DataPath)
        line = f.readline()
        kpoints = []
        gruneisen_list = []
        frequency_list = []
        n_list = []
        i = 0
        j = 0
        npath = 0
        while line:
            if re.search("- nqpoint:",line):
                i = 1
                npath += 1

            if i == 1 and re.search("- q-position:",line):
                k = pattern2.findall(line)
                k = map(float,k)
                i = 0
                if npath == 1:
                    kpoints.append(k)
            elif i == 0 and re.search("- q-position:",line):
                k = pattern2.findall(line)
                k = map(float,k)
                kpoints.append(k)

            if re.search("distance:",line):
                j = pattern2.findall(line)
                j = float(j[0])
            if j == 0 and npath == 1:
                criterion = 1
            elif j != 0:
                criterion = 1
            else:
                criterion = 0
            if criterion == 1 and re.search("gruneisen:",line):
                gruneisen = pattern2.findall(line)
                gruneisen = float(gruneisen[0])
                gruneisen_list.append(gruneisen)
            elif criterion == 1 and re.search("frequency:",line):
                frequency = pattern2.findall(line)
                frequency = float(frequency[0])
                frequency_list.append(frequency)
            elif re.search("- #",line):
                n = pattern1.findall(line)
                n = int(n[0])
                n_list.append(n)
            line = f.readline()
        f.close()

        nbands = max(n_list)
        nkpoints  =len(kpoints)
        r = self.omega(nkpoints,nbands,gruneisen_list)
        w = self.omega(nkpoints,nbands,frequency_list)

        qnodes = self.k_nomalizer(kpoints,npath,x,y,z)[0]
        qpoints = self.k_nomalizer(kpoints,npath,x,y,z)[1]

        return qpoints,r,w,qnodes,nbands,nkpoints,npath

#gd = geda()
#path = '/Users/liusongwei/Titanium/mode_Gruneisen_parameters/result_fdm_G_test4/alpha/gruneisen.yaml'
#print(gd.GetGruneisen(path))
#print(gd.GetPhononBands(path)[0])
#print(gd.GetPhononBands(path)[2])