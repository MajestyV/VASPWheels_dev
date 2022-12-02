from VaspWheels import GetKpath

GK = GetKpath.Kpath()  # 调用GetKpath模块

saving_address = 'D:/Projects/PhaseTransistor/Data/Simulation/Conductivity/Kpath_files/K-path_ORT_2'
# Gamma-M-K-Gamma-A-L-H-A
# path = [[0, 0, 0], [0.5, 0, 0], [1.0 / 3.0, 1.0 / 3.0, 0], [0, 0, 0], [0,0,1/2.0], [1/2.0,0,1/2.0], [1/3.0, 1/3.0, 1/2.0], [0,0,1/2.0]]
# Gamma-X-S-Y-Gamma-A
nodes = [[0, 0, 0], [0.5, 0, 0], [0.5, 0.5, 0], [0, 0, 0], [0, 0.5, 0]]
a = GK.GetKpath(saving_address,nodes,99)