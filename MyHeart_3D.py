import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

def r(theta,a=1.2,R0=1):
    if isinstance(theta,list):
        radius = []
        for n in theta:
            if np.pi/2 <= n < 3*np.pi/2:
                radius.append(R0 + a * n)
            elif 3*np.pi/2 < n <= 5*np.pi/2:
                radius.append(R0 + (3*np.pi-n) * a)
    else:
        radius = 0
        if np.pi/2 <= theta < 3*np.pi/2:
            radius = R0+a*theta
        elif 3*np.pi/2 < theta <= 5*np.pi/2:
            radius = R0+(3*np.pi/2-theta)*a
    return radius

angle = list(np.linspace(np.pi/2,5*np.pi/2,200))
R = r(angle)
# plt.plot(angle,r(angle))

h = 1.0
z = list(np.linspace(-h,h,50))
coordinate = []
for i in range(len(z)):
    print(z[i])
    for j in range(len(angle)):
        Rz = R[j]*np.sqrt(1-z[i]**2/h**2)
        coordinate.append([Rz,angle[j],z[i]])
X = []
Y = []
Z = []
for k in range(len(coordinate)):
    X.append(coordinate[k][0]*np.cos(coordinate[k][1]))
    Y.append(coordinate[k][0]*np.sin(coordinate[k][1]))
    Z.append(coordinate[k][2])

#x = []
#y = []
#for i in range(len(angle)):
    #x.append(R[i]*np.cos(angle[i]))
    #y.append(R[i]*np.sin(angle[i]))
#plt.plot(x,y)
#plt.xlim(-8,8)
#plt.ylim(-8,8)

fig = plt.figure()
ax1 = Axes3D(fig)
ax1.scatter(X,Y,Z)
# print(coordinate)