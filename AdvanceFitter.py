import numpy as np

class CubicSpline:
    def __init__(self,x,y):
        self.x = x
        self.y = y

    def NaturalCuSp(self):
        x = self.x
        a = self.y
        n = len(x)-1

        h, alpha = [], []
        alpha.append(0)
        for i in range(n):
            h.append(x[i+1]-x[i])
            if i >= 1:
                alpha.append(3*(a[i+1]-a[i])/h[i]-3*(a[i]-a[i-1])/h[i-1])

        l, u, z = [], [], []
        l.append(1)
        u.append(0)
        z.append(0)
        for i in range(1,n):
            l.append(2*(x[i+1]-x[i-1])-h[i-1]*u[i-1])
            u.append(np.float(h[i])/l[i])
            z.append((alpha[i]-h[i-1]*z[i-1])/l[i])
        l.append(1)
        z.append(0)
        c = [0 for i in range(n+1)]
        b, d = [0 for i in range(n)], [0 for i in range(n)]
        for i in range(n):
            j = n-1-i
            c[j] = z[j]-u[j]*c[j+1]
            b[j] = (a[j+1]-a[j])/h[j]-h[j]*(c[j+1]+2*c[j])/3
            d[j] = (c[j+1]-c[j])/(3*h[j])

        return a,b,c,d