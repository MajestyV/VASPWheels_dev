import numpy as np

a = [1,2,3]
a2 = [3,2,1]

b = [[1,1,1],
     [2,2,2],
     [3,3,3]]

c = np.zeros(3)

c = [0,1,1]

print(np.outer(a,a2))
print(np.cross(a,a2))
# print(np.inner(a,b))
# print(np.outer(a,b))

print(np.zeros(3))