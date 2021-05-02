from mpl_toolkits import mplot3d
import matplotlib.pyplot as plt
import kinematic_model as km
import numpy as np
import math as m

plt.rcParams.update({'font.size': 12})

### plot posselt figure ###
xs = []
zs = []
ox = []
oz = []

# plot IP envelope
# in saggital plane (max opening)
# in frontal plane (max laterotrusion and max opening)

# vertical 50 / lateral 12 / horizontal 15

# alpha: -4 to 4 -> depends on gamma
# beta: mean max value about 34° for opening (see non-orthogonal...) ? and compare to artisynth
# gamma: -10 to 10
# x: 0-15 for 15 mm horizontal translation
# y: -6 to 6
# z: -7 to 0 directly depends on x and on the slope -> min value of the slope for range of x is max z range

def fw_km(x, y, beta, gamma):
    o, pos = km.forward_kinematics_4DOF(x, y, np.radians(beta), np.radians(gamma))
    x, y, z, _ = pos
    ox.append(o[0])
    oz.append(o[2])
    xs.append(x)
    zs.append(z)
    return o, z

beta = 0
for i in range(20):
    # first 20mm are pure rotation
    o, z = fw_km(0, 0, i, 0)
    if z < km.inc_init[2]-20:
        beta = i
        break

# beta is then 16 degrees, opening distance 20
for i in range(15):
    # for each mm translation, 1.2 degrees rotation, 1.2 chosen so that at 15mm translation, beta will be at max (1.2 consistent with paper specificity)
    fw_km(i, 0, beta+i*1.2, 0)

# at max x, beta position
fw_km(15, 0, 34, 0)

#print("min z:")
#print(o[2])
#print("max z displacement:")
#print(km.inc_init[2]-z)

# beta = -4: mandible in maximum protrusion, lower teeth overlap upper teeth
# -4 so that lower incisors can be same height as upper incisors at max protrusino
for i in range(34, -4, -1):
    fw_km(15, 0, i, 0)

for i in range(15, -1, -1):
    beta = -4 + 4/15*(15-i)
    fw_km(i, 0, beta, 0)

plt.plot(ox, oz, c="r", label="condylar slope")
plt.plot(xs, zs, label="IP")
plt.legend()
plt.xlabel("X (mm)")
plt.ylabel("Z (mm)")
plt.axis("equal")

# plot angle
min_o, min_IP = km.forward_kinematics_4DOF(0, 0, np.radians(0), np.radians(0))
max_o, max_IP = km.forward_kinematics_4DOF(15, 0, np.radians(34), np.radians(0))

plt.plot([max_o[0], min_IP[0]], [max_o[2], min_IP[2]], ls='dashed', c='grey')
plt.plot([max_o[0], max_IP[0]], [max_o[2], max_IP[2]], ls='dashed', c='grey')

theta = np.linspace(-np.pi/3, -np.pi/7, 20)

r = 20 # circle radius

x1 = r * np.cos(theta) + max_o[0]
x2 = r * np.sin(theta) + max_o[2]

plt.plot(x1, x2, color='gray', ls='dashed')
plt.text(max_o[0]+8, max_o[2]-11, '34.0°', fontsize=8, color='grey')

plt.show()

# reaches 42 mm z displacement (not 50)
# and 15 horizontal

# posselt in frontal plane

ys = []
zs = []
oy = []
oz = []

# no literature values
# max laterotrusion at small opening (20) and forward translation (7.5) (see posselt pic)
# condylar lateral displacement is very small because anatomically constrained
# therefore most of movement with gamma rotation, not much needed to reach 12mm lateral movement range

for i in range(10):
    o, pos = km.forward_kinematics_4DOF(4, 0, np.radians(0), np.radians(i))
    x, y, z, _ = pos
    oy.append(o[1])
    oz.append(o[2])
    ys.append(y)
    #print(y)
    zs.append(z)

plt.plot(oy, oz, c="r", label="condylar slope")
plt.plot(ys, zs, label="IP")
plt.legend()
plt.xlabel("Y (mm)")
plt.ylabel("Z (mm)")
plt.axis("equal")
#plt.show()
