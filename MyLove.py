from Wheels import functions
import matplotlib.pyplot as plt

MyLove = functions.fx()

l = MyLove.MyHeart(a=1,r0=0)

l1 = []
for i in range(len(l[1])):
    l1.append(l[1][i]*9.8/7.3)


plt.plot(l[0],l1)
#plt.plot(l[0],l[2])
plt.xlim(-6,6)
plt.ylim(-6,6)
plt.savefig('/Users/liusongwei/Desktop/MyLove_MyHeart.png')