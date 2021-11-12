from Wheels import GetData
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt

geda = GetData.geda()

file = "/Users/liusongwei/MaterialsGallery/MoS2/DOS_test/MoS2-2H/DOSCAR"

dos = geda.GetEDOS(file)

print(dos)

x = []
yup = []
ydn = []
for i in range(len(dos)):
    x.append(dos[i][0])
    yup.append(dos[i][1])
    ydn.append(dos[i][2])
plt.plot(x,yup)
#plt.plot(x,ydn)
plt.xlim(-10,6)
plt.ylim(0,30)