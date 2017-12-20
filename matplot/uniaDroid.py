import matplotlib
matplotlib.use('Agg')  
from mpl_toolkits.mplot3d import axes3d  
import numpy as np
import matplotlib.pyplot as plt  
from matplotlib import cm  
      
inFile = open('/home/y00211003/10001001001.txt', 'r')

x0 = []
y0 = []

for line in inFile:
    trainingSet = line.split(':')
    x0.append(trainingSet[0])
    y0.append(trainingSet[1])

length = len(y0)
if length>10:
    x = x0[(length-10):]
    y = y0[(length-10):]
else:
    x = x0
    y = y0
X = [int(i) for i in x]
Y = [float(i)/1000.000 for i in y]

inFile2 = open('/home/y00211003/10001001002.txt', 'r')
z0 = []
for line2 in inFile2:
    trainingSet = line2.split(':')
    z0.append(trainingSet[1])
if length>10:
    z = z0[(length-10):]
else:
    z = z0
Z = [float(i)/1000.000 for i in z]

inFile3 = open('/home/y00211003/10001001003.txt', 'r')
w0 = []
for line3 in inFile3:
    trainingSet = line3.split(':')
    w0.append(trainingSet[1])
if length>10:
    w = w0[(length-10):]
else:
    w = w0
W = [float(i)/1000.000 for i in w]

print Y
print Z
print W
#plt.figure(1)

#plt.plot(X, y, 'rx')
#plt.xlabel('VMI server version')
#plt.ylabel('realDeviceLoginTime_ms')

#plt.show()

n_groups = len(X)
fig, ax = plt.subplots()
index = np.arange(n_groups)+1
bar_width = 0.25
opacity = 0.4
rects1 = plt.bar(index-bar_width-bar_width, Y, bar_width, alpha=opacity, align='center', color='b', label='user_10001001001')
rects2 = plt.bar(index-bar_width, Z, bar_width, alpha=opacity, align='center', color='r', label='user_10001001002')
rects3 = plt.bar(index, W, bar_width, alpha=opacity, align='center', color='g', label='user_10001001003')
plt.xlabel('VMI_version_Latest10')  
plt.ylabel('uniaBootTime_second')  
plt.title('UniaBootTime_Parallel')  
#plt.xticks(index + bar_width, X)
plt.xticks(index, X, rotation=90)

#plt.bar(X,Y,width = 0.35,facecolor = 'lightskyblue',edgecolor = 'white')
m = np.array(list(X))
n = np.array(list(Y))
n2 = np.array(list(Z))
n3 = np.array(list(W))
for x1,y1 in zip(index,n):
    plt.text(x1-bar_width-bar_width, y1+0.05, '%.2f' % y1, ha='center', va= 'bottom', fontsize= 7, rotation=90)

for x2,y2 in zip(index,n2):
    plt.text(x2-bar_width, y2+0.05, '%.2f' % y2, ha='center', va= 'bottom', fontsize= 7, rotation=90)

for x3,y3 in zip(index,n3):
    plt.text(x3, y3+0.05, '%.2f' % y3, ha='center', va= 'bottom', fontsize= 7, rotation=90)

plt.ylim(0,12)  
plt.legend()  
  
plt.tight_layout() 

plt.show() 
plt.savefig('/home/y00211003/uniaLoginTime.png')


