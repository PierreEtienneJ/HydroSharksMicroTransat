import numpy as np
import random
import math
import matplotlib.pyplot as plt
import sys 

def f(x, a=0.1, b=0.1, c=1):
    return a*x**2+b*x+c


A=[f(0, 0.1, 0.1,1)]
X=[i for i in range(10)]
for i in range(len(X)-1):
    A.append(A[-1]+f(X[i], 0.1, 0.1, 1))
    


#plt.plot(X, [f(X[i], 0.1, 0.1, 1) for i in range(len(X))], "r")
#plt.plot(X, A , "b")
#plt.show()

""" import matplotlib.pyplot as plt
import time
import random
 
ysample = random.sample(range(-50, 50), 100)
 
xdata = []
ydata = []
 
plt.show()
 
axes = plt.gca()
axes.set_xlim(0, 100)
axes.set_ylim(-50, +50)
line, = axes.plot(xdata, ydata, 'r-')
 
for i in range(100):
    xdata.append(i)
    ydata.append(ysample[i])
    line.set_xdata(xdata)
    line.set_ydata(ydata)
    plt.draw()
    plt.pause(1e-17)
    time.sleep(0.01)
 
# add this if you don't want the window to disappear at the end
plt.show() """

import matplotlib.pyplot as plt
import time
import random
from mpl_toolkits import mplot3d
import numpy as np


def g(v,theta):
    if(-5<theta<5):
        x= 0
    elif(-20<theta<20):#hormis [-5, 5]
        if(theta>0):
            #coef droite
            A=np.array(([5,1],[20, 1]))
            Y=np.array((0, 2))
            X=np.dot(np.linalg.inv(A),Y)
            a=X[0]
            b=X[1]
            x=a*theta+b
        else:
            A=np.array(([-5,1],[-20, 1]))
            Y=np.array((0, 2))
            X=np.dot(np.linalg.inv(A),Y)
            a=X[0]
            b=X[1]
            x=a*theta+b            
    else:
        if(theta>0):
            A=np.array(([100**2, 100, 1],[180**2, 180, 1], [20**2, 20, 1]))
            Y=np.array((4, 2, 2))
            X=np.dot(np.linalg.inv(A),Y)
            a=X[0]
            b=X[1]
            c=X[2]
            x=a*theta**2+b*theta+c
        else:
            A=np.array(([100**2, -100, 1],[180**2, -180, 1], [20**2, -20, 1]))
            Y=np.array((4, 2, 2))
            X=np.dot(np.linalg.inv(A),Y)
            a=X[0]
            b=X[1]
            c=X[2]
            x=a*theta**2+b*theta+c
    v=abs(v)
    A=np.array(([30**2, 30, 1],[10**2, 10, 1], [50**2, 50, 1]))
    Y=np.array((4, 1, 3))
    X=np.dot(np.linalg.inv(A),Y)
    a=X[0]
    b=X[1]
    c=X[2]
    y=a*theta**2+b*theta+c
    return x*y

v=np.linspace(0,100, 100)
t=np.linspace(-180, 180, 100)

fig=plt.figure()
ax=plt.axes(projection='3d')

for j in range(100):
    z=np.zeros(100)
    for i in range(100):
        z[i]=g(v[j], t[i])
    ax.scatter(v, t, z)



plt.xlabel("vitesse vent")
plt.ylabel("theta")
plt.show()