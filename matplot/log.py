import matplotlib
matplotlib.use('Agg')  
from mpl_toolkits.mplot3d import axes3d  
import numpy as np
import matplotlib.pyplot as plt  
from matplotlib import cm  
      
inFile = open('/home/y00211003/droidLoginTime.txt', 'r')

x = []
y = []

for line in inFile:
    trainingSet = line.split(':')
    x.append(trainingSet[0])
    y.append(trainingSet[1])

length = len(y)


X = [int(i) for i in x]
Y = [float(i)/1000.000 for i in y]

print Y
#plt.figure(1)

#plt.plot(X, y, 'rx')
#plt.xlabel('VMI server version')
#plt.ylabel('realDeviceLoginTime_ms')

#plt.show()

n_groups = len(X)
fig, ax = plt.subplots()
index = np.arange(n_groups)+1
bar_width = 0.35
opacity = 0.4
rects1 = plt.bar(index, Y, bar_width, alpha=opacity, align='center', color='b', label='LoginTime')
plt.xlabel('VMI_version')  
plt.ylabel('realDeviceLoginTime_second')  
plt.title('LoginTimeHistory')  
#plt.xticks(index + bar_width, X)
plt.xticks(index, X)

#plt.bar(X,Y,width = 0.35,facecolor = 'lightskyblue',edgecolor = 'white')
m = np.array(list(X))
n = np.array(list(Y))
for x1,y1 in zip(index,n):
    plt.text(x1, y1+0.05, '%.2f' % y1, ha='center', va= 'bottom', fontsize= 7)

plt.ylim(0,30)  
plt.legend()  
  
plt.tight_layout() 

plt.show() 
plt.savefig('/home/y00211003/realDeviceLoginTime.png')


