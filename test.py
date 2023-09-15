import VaspWheels as vw

data = [0,1,2,3,4,5,6,7,8,9]

data_filtered = vw.Experiment.Moving_average(data,3)

print(data_filtered)