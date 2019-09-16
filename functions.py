import numpy as np
from scipy import integrate

class fx:
    def __init__(self,NA=6.022e+23,kB=1.38e-23,hbar=1.055e-34,d=3):
        self.NA = NA
        self.kB = kB
        self.hbar = hbar
        self.d = d # d for dimension

    def integration(self,y,x):
        omnia = 0
        for i in range(0, len(x)-1):
            if i == 0:
                omnia += (x[i+1]-x[i])*y[i]/2
            elif i == len(x):
                omnia += (x[i]-x[i-1])*y[i]/2
            else:
                omnia += (x[i+1]-x[i-1])*y[i]/2
        return omnia

    def HFE(self,T,na,p,w): # Helmholz Free Energy. p is DOS and w is Vibration Frequency.
        Nd = self.NA/na
        tos = integrate.trapz(p, w)
        lnZ = Nd*na*self.d*np.log(self.kB*T/self.kB)-Nd*integrate.trapz(p*np.log(w),w)*na*self.d/tos
        f = -self.kB*T*lnZ
        return f

    def TransTemp(self,Ea,pa,wa,Eb,pb,wb):
        tosa = integrate.trapz(pa,wa) # TOS of a-phase
        tosb = integrate.trapz(pb,wb) # TOS of b-phase
        Sab = -self.NA*self.d*self.kB*(integrate.trapz(pb*np.log(wb),wb)/tosb-integrate.trapz(pa*np.log(wa),wa)/tosa)
        Eab = Eb-Ea
        Temp = Eab/Sab
        return Temp