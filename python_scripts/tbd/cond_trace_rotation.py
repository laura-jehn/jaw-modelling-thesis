from mpl_toolkits import mplot3d

import numpy as np
import math
import matplotlib.pyplot as plt

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

fig = plt.figure()
#ax = plt.axes(projection="3d")
#ax.plot3D(x, y, z)

x_displacement = [n+51.7785 for n in x]
y_displacement = [-round(n-31.4501,2) for n in y]
z_displacement = [round(n-79.637,2) for n in z]

#print(max(x_displacement)) # during opening-closing 0.0026464944163

# x values are zero
plt.title("condylar trace (right condyle)")
plt.ylabel("Z values (downwards)")
plt.xlabel("Y values (protrusion)")
plt.plot(y_displacement, z_displacement)
plt.axis('square')
plt.show()


## determine phi_1, rotation angle around condylar axis

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
tmj_y_li = [li-c for li, c in zip(y_li, y)]
tmj_z_li = [li-c for li, c in zip(z_li, z)]
#upper incisor constant
ui = [-48.3688, 43.449299999999994] #x is zero
#upper incisor coordinates relative to the condyle
tmj_y_ui = [ui[0]-c for c in y]
tmj_z_ui = [ui[1]-c for c in z]

#angle in y-z plane
angle = [0]
#vector u is position of lower incisors at the beginning
u = np.array([tmj_y_li[0], tmj_z_li[0]])

for i in range(1, len(x)):
    v = np.array([tmj_y_li[i], tmj_z_li[i]])
    angle.append(math.degrees(math.acos((np.dot(u,v)/np.linalg.norm(u)/np.linalg.norm(v)))))

#print(angle)

f = open("../artisynth_models/src/artisynth/models/dynjaw/data/ConTrace/mouthOpeningAngle.txt", "r")
lines = f.readlines()
simulation_angle = []

for l in lines[2:]:
    p = l.split(' ')
    simulation_angle.append(float(p[2]))

f.close()
#print(simulation_angle)
#print(len(simulation_angle))

fig = plt.figure()
plt.title("Mouth Opening Angle During Mouth Opening Movement")
plt.ylabel("angle in degrees, measured around the condylar axis")

plt.plot(range(0, 201, 2), simulation_angle[0:101], label="opening angle to upper incisors")
plt.plot(angle, color="red", label="condylar rotation")
plt.legend()
plt.show()

# next step: take angle and displacement values to calculate end effector position, then compare with general lowinc_trace
