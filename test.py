import numpy as np

a = [1,2,3]
a2 = [3,2,1]

b = [[1,1,1],
     [2,2,2],
     [3,3,3]]

c = [[1,0,0],
     [0,2,0],
     [0,0,3]]

#print(np.outer(a,a2))
#print(np.cross(a,a2))
# print(np.inner(a,b))
# print(np.outer(a,b))

#print(np.zeros(3))

print(np.array([a])@np.array(c)@np.array([a]).T)