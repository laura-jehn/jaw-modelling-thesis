from mpl_toolkits import mplot3d
import matplotlib.pyplot as plt
import kinematic_model as km
import numpy as np
import math as m

plt.rcParams.update({'font.size': 12})

### plot posselt envelope in the sagittal plane ###

xs = []
zs = []
ox = []
oz = []

# helper function for calling forward kinematics
def fw_km(x, y, beta, gamma):
    mTi, pos = km.forward_kinematics_4DOF(x, y, np.radians(beta), np.radians(gamma))
    x, y, z, _ = pos
    o = mTi[:,3]
    ox.append(o[0])
    oz.append(o[2])
    xs.append(x)
    zs.append(z)
    return o, x, z

# first 20mm opening are pure rotation, 20mm correspond to beta = 16 degrees
beta = 0
for i in range(20):
    o, x, z = fw_km(0, 0, i, 0)
    if i==0:
        plt.annotate('A', xy=(x, z), xytext=(x, z+1.5), c='C0')
    if z < km.inc_init[2]-20:
        beta = i
        break

plt.annotate('B', xy=(x, z), xytext=(x-4, z), c='C0')

for i in range(15):
    # for each mm translation, 1.2 degrees rotation
    fw_km(i, 0, beta+i*1.2, 0)

# at max x, max beta position
o, x, z = fw_km(15, 0, 34, 0)

plt.annotate('C', xy=(x, z), xytext=(x-4, z-1), c='C0')

# beta = -4: mandible in maximum protrusion, lower teeth overlap upper teeth
# -4 so that lower incisors can be same height as upper incisors at max protrusion
for i in range(34, -4, -1):
    o, x, z = fw_km(15, 0, i, 0)

plt.annotate('D', xy=(x, z), xytext=(x, z+2.5), c='C0')

for i in range(15, -1, -1):
    beta = -4 + 4/15*(15-i)
    o, x, z = fw_km(i, 0, beta, 0)

plt.plot(ox, oz, c="r", label="condylar slope")
plt.plot(xs, zs, label="IP")
plt.legend()
plt.xlabel("X (mm)")
plt.ylabel("Z (mm)")
plt.axis("equal")

# plot angle (deprecated)
mTi_min, min_IP = km.forward_kinematics_4DOF(0, 0, np.radians(0), np.radians(0))
mTi_max, max_IP = km.forward_kinematics_4DOF(15, 0, np.radians(34), np.radians(0))

min_o = mTi_min[:,3]
max_o = mTi_max[:,3]

#plt.plot([max_o[0], min_IP[0]], [max_o[2], min_IP[2]], ls='dashed', c='grey')
#plt.plot([max_o[0], max_IP[0]], [max_o[2], max_IP[2]], ls='dashed', c='grey')

theta = np.linspace(-np.pi/3, -np.pi/7, 20)

r = 20 # circle radius

x1 = r * np.cos(theta) + max_o[0]
x2 = r * np.sin(theta) + max_o[2]

#plt.plot(x1, x2, color='gray', ls='dashed')
#plt.text(max_o[0]+7, max_o[2]-11, '34.0°', fontsize=10, color='grey')

plt.show()
