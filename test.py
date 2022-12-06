import numpy as np
from VaspWheels import Crystallography
from VaspWheels import GetKpath

CT = Crystallography.Crystal()
GK = GetKpath.vasp()

lattice = ['Cubic', [1, 1, 1, 90, 90, 90], 'primitive']

real_lattice = [[3.147329567, 0.000000000, 0.000000000],
                [-1.573664783, 2.725667359, 0.000000000],
                [0.000000000, 0.000000000, 43.912290363]]

# 会跟VASP的OUTCAR差2pi倍
lattice_reciprocal = CT.Reciprocal_lattice('HEX',[3.147329567,3.147329567,43.912290363,90,90,120])
# lattice_reciprocal = CT.Reciprocal_lattice('HEX',[3.147329567,3.147329567,1,90,90,120])
a = GK.CalculateReciprocalLattice(real_lattice)

print(lattice_reciprocal)
print(a)

print((1/4.0)*0.176666666667/(1/6.0))