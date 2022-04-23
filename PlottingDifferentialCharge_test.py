from py4vasp import Calculation

calc = Calculation.from_path('/Users/liusongwei/MaterialsGallery/MoS2/Data/GSE/3_D3BJ_GSE_1/0.025')

a = calc.dos.plot()

print(a)

