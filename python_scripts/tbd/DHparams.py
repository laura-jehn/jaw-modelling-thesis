## DH parameters ##
import numpy as np
import math

dh_params = open("DHparams.txt", "w")
dh_params.write("theta1 d2 d3 d4\n\n")

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

#angle in y-z plane
angle = [0]
#vector u is position of lower incisors at the beginning
u = np.array([tmj_y_li[0], tmj_z_li[0]])

for i in range(1, len(x)):
    v = np.array([tmj_y_li[i], tmj_z_li[i]])
    angle.append(math.degrees(math.acos((np.dot(u,v)/np.linalg.norm(u)/np.linalg.norm(v)))))

for i in range(200):
    dh_params.write("{0} {1} {2} {3}\n".format(angle[i], x_displacement[i], z_displacement[i], y_displacement[i]))

dh_params.close()
# next step: take angle and displacement values to calculate end effector position, then compare with general lowinc_trace
