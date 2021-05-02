from mpl_toolkits import mplot3d

import numpy as np
import math
import matplotlib.pyplot as plt

f_rtmj = '../artisynth_core/scripts/rtmjTraceOWMA.txt'
f_ltmj = '../artisynth_core/scripts/ltmjTraceOWMA.txt'
f_li = '../artisynth_core/scripts/liTraceOWMA.txt'

f_array = [f_rtmj, f_ltmj, f_li]

pos_rtmj = [[] for _ in range(3)] # 3 empty arrays for x, y and z coordinates
pos_ltmj = [[] for _ in range(3)]
pos_li = [[] for _ in range(3)]

with open(f_rtmj, "r") as f:
    for l in f:
        ln = l.strip()
        points = l.split(" ")
        [pos_rtmj[x].append(float(points[x])) for x in range(len(points))]

with open(f_ltmj, "r") as f:
    for l in f:
        ln = l.strip()
        points = l.split(" ")
        [pos_ltmj[x].append(float(points[x])) for x in range(len(points))]

with open(f_li, "r") as f:
    for l in f:
        ln = l.strip()
        points = l.split(" ")
        [pos_li[x].append(float(points[x])) for x in range(len(points))]


#condylar trace
fig = plt.figure()
ax = fig.add_subplot(1, 1, 1, projection='3d')
plt.title("condyle and incisor trajectory during opening")
ax.plot(pos_ltmj[0], pos_ltmj[1], pos_ltmj[2], c='r', label="condyle")
ax.plot(pos_rtmj[0], pos_rtmj[1], pos_rtmj[2], c='r', label="condyle")
ax.plot(pos_li[0], pos_li[1], pos_li[2], c='b', label="incisor")
ax.legend()
ax.set_xlabel("x")
ax.set_ylabel("y")
ax.set_zlabel("z")
plt.axis('square')
plt.show()

#calculate moving distance of condyles
rtmj_diff_x = pos_rtmj[1][len(pos_rtmj[1])-1] - pos_rtmj[1][0]
rtmj_diff_z = pos_rtmj[2][len(pos_rtmj[2])-1] - pos_rtmj[2][0]
print(rtmj_diff_x, rtmj_diff_z)
