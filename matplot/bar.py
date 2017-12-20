import matplotlib
# Force matplotlib to not use any Xwindows backend.
matplotlib.use('TkAgg')

import numpy as np
from matplotlib import pyplot as plt

inFile = open('/home/y00211003/droidLoginTime.txt', 'r')

X1 = []
Y1 = []

for line in inFile:
    trainingSet = line.split('.')
    X1.append(trainingSet[0])
    Y1.append(trainingSet[1])
length = len(Y1)

X = [int(i) for i in X1]
Y = [int(i) for i in Y1]

plt.figure(figsize=(9,6))
#plt.figure(1)
#n = 8
X = np.arange(length)+1
#Y1 = np.random.uniform(0.5,1.0,n)
#Y2 = np.random.uniform(0.5,1.0,n)
plt.bar(X,Y,width = 0.35,facecolor = 'lightskyblue',edgecolor = 'white')
#plt.bar(X+0.35,Y2,width = 0.35,facecolor = 'yellowgreen',edgecolor = 'white')
for x,y in zip(X,Y):
    plt.text(x, y, '%s', ha='center', va= 'bottom')

#for x,y in zip(X,Y2):
#    plt.text(x+0.6, y+0.05, '%.2f' % y, ha='center', va= 'bottom')
plt.ylim(0,+1.25)
plt.show()
plt.savefig('/home/y00211003/bar001.png')
