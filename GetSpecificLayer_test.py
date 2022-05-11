from VaspWheels import LatticeOperation

lt = LatticeOperation.latte()

POSCAR = 'D:/MaterialsGallery/2D Materials/MoS2/Crystal structures/2H_Testing/MoS2_bulk.vasp'
# 不知道为啥，这个包会更新输入的值，所以最好每次都重新读一边bulk的数据
crystal_intel = lt.ReadPOSCAR(POSCAR)
a, b, c = crystal_intel
for n in range(10):
    n_layer = n+1
    print(a)
    saving_directory = 'D:/MaterialsGallery/2D Materials/MoS2/Crystal structures/2H_Testing/MoS2_'+str(n_layer)+'.vasp'
    if n != 0:
        a_new, b_new = lt.ExfoliateFewLayer(n_layer,20,a,b)
    else:
        a_new, b_new = lt.Exfoliate(20,a,b)
    lt.WritePOSCAR(saving_directory, a_new, b_new, c)