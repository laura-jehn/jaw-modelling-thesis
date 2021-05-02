# analyze chewing

from mpl_toolkits import mplot3d

import numpy as np
import math
import matplotlib.pyplot as plt


### CONDYLE DURING CHEWING ###

f = open("../artisynth_core/scripts/rtmj_trace.txt", "r")
lines = f.readlines()
x = []
y = []
z = []

for l in lines:
    p = l.split(' ')
    x.append(float(p[0]))
    y.append(float(p[1]))
    z.append(float(p[2]))

f.close()

x_displacement = [round(n+51.7785,4) for n in x]
y_displacement = [-round(n-31.4501,4) for n in y]
z_displacement = [round(n-79.637,4) for n in z]


### LOWER INCISORS DURING CHEWING ###

f = open("../artisynth_core/scripts/lowinc_trace.txt", "r")
lines = f.readlines()
x_li = []
y_li = []
z_li = []

for l in lines:
    p = l.split(' ')
    x_li.append(float(p[0]))
    y_li.append(float(p[1]))
    z_li.append(float(p[2]))

f.close()

#lower incisor coordinates relative to the condyle
print(x, y, z)

tmj_x_li = [li-c for li, c in zip(x_li, x)]
tmj_y_li = [li-c for li, c in zip(y_li, y)]
tmj_z_li = [li-c for li, c in zip(z_li, z)]


fig = plt.figure()

plt.subplot(1, 2, 1)
plt.title("lower incisor trace")
plt.plot(x_li, y_li)
plt.xlabel("x")
plt.ylabel("y")
plt.subplot(1, 2, 2)
plt.title("relative to condyle")
plt.xlabel("x")
plt.ylabel("y")
plt.plot(tmj_x_li, tmj_y_li)
#plt.axis('square')
plt.show()

#fig = plt.figure()
#plt.show()

#plt.subplot(1,2,1)
#ax = plt.axes(projection="3d")
#plt.axis('square')
#ax.plot3D(y_displacement, x_displacement, z_displacement)
#plt.show()

#
#plt.title("condylar trace during chewing (right condyle)")
#plt.ylabel("Z values (downwards)")
#plt.xlabel("Y values (protrusion)")
#plt.plot(y_displacement, z_displacement)
#plt.axis('square')

#plt.subplot(1, 3, 1)
#plt.plot(x_displacement[0:70], y_displacement[0:70])
#plt.title("From Above")
#plt.xlabel("X values (laterally)")
#plt.axis(xlim=(-1, 1))
