import numpy as np
from scipy import integrate
from scipy.misc import derivative

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

    def Volume(self,lv,na=""):
        if not na:
            n = 1
        else:
            n = na
        v = lv[0,0]*(lv[1,1]*lv[2,2]-lv[2,1]*lv[1,2])+lv[0,1]*(lv[1,2]*lv[2,0]-lv[2,2]*lv[1,0])+lv[0,2]*(lv[1,0]*lv[2,1]-lv[2,0]*lv[1,1])
        vpa = v/n # Volume per atom
        return vpa

    def MyHeart(self,a=1.5,b=1,r0=1,n=1314):
        theta = np.linspace(0.5*np.pi,2.5*np.pi,1000)
        #theta = b*t
        radius = r0
        dt = theta[1]-theta[0]
        r = []
        for i in range(len(theta)):
            if theta[i] <= 1.5*np.pi:
                radius += a*dt
            else:
                radius += -a*dt
            r.append(radius)
        x = []
        y = []
        for i in range(len(theta)):
            x.append(r[i]*np.cos(theta[i]))
            y.append(r[i]*np.sin(theta[i]))
        return x,y

class BirchMurnaghanEOS:
    def __init__(self,V="",P="",E=""):
        self.V = V
        self.P = P
        self.E = E

    def BulkModulus(self,V="",P="",dP=""):
        if V[0]:
            Vol = V
            Press = P
        else:
            Vol = self.V
            Press = self.P
        if dP:
            Pstep = dP # dP = step of pressure
        else:
            Pstep = Press[1]-Press[0]

        def f(x): return Vol[Press.index(x)]

        dP_list = []
        B_list = []
        for i in range(1,len(Press)-1):
            x = Press[i]
            dP_list.append(1/derivative(f,x,dx=Pstep))
            B_list.append(-Vol[i]/derivative(f,x,dx=Pstep))
            if x == 0:
                dP0 = derivative(f,x,dx=Pstep)

        def g(y): return B_list[Press.index(y)-1]

        dB_list = []
        for j in range(2,len(B_list)-1):
            y = Press[j]
            dB_list.append(derivative(g,y,dx=Pstep))
            if y == 0:
                dB0 = derivative(g,y,dx=Pstep)

        B0 = -Vol[Press.index(0)]/dP0

        return B0,dB0

    def V_P_curve(self,V="",P=""):
        if V[0]:
            Vol = V
            Press = P
        else:
            Vol = self.V
            Press = self.P
        V0 = Vol[Press.index(0)]
        B0 = self.BulkModulus(Vol,Press)[0]
        dB0 = self.BulkModulus(Vol,Press)[1]
        Fitted_P_list = []
        for i in range(len(Vol)):
            Fitted_P = 3*B0*((V0/Vol[i])**(7.0/3.0)-(V0/Vol[i])**(5.0/3.0))*(1+3*(dB0-4)*((V0/Vol[i])**(2.0/3.0)-1))/2
            Fitted_P_list.append(Fitted_P)
        return Fitted_P_list

    def V_E_curve(self,V="",E="",P=""):
        if V[0]:
            Vol = V
            Energy = E
            Press = P
        else:
            Vol = self.V
            Energy = self.E
            Press = self.P
        E0 = min(Energy)
        V0 = Vol[Energy.index(E0)]
        B0 = self.BulkModulus(Vol, Press)[0]/160.2
        dB0 = self.BulkModulus(Vol, Press)[1]
        Fitted_E_list = []
        for i in range(len(Vol)):
            #a = (V0/Vol[i])**(2.0/3.0)-1
            #Fitted_E = E0+9*V0*B0*(dB0*a**3+(6-4*(a+1))*a**2)/16
            Fitted_E = E0+B0*Vol[i]*((V0/Vol[i])**dB0/(dB0-1)+1)/dB0-B0*V0/(dB0-1)
            Fitted_E_list.append(Fitted_E)
        return Fitted_E_list