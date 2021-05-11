from mpl_toolkits import mplot3d
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import math as m

plt.rcParams.update({'font.size': 14})

#limited ROM
muscle_force = [1, 0.5, 0.4, 0.2, 0.15, 0.1, 0.05, 0.01, 0.005, 0.0]
opening_distance = [38.82, 37.97, 37.57, 35.71, 34.53, 32.26, 25.14, 15.45, 13.19, 8.62] # max mouth opening distances at 100% muscle activation

fig = plt.figure()
#plt.title("")
plt.subplot(1,2,1)
plt.xlabel("Percentage of maximum muscle force")
plt.ylabel("Maximum mouth opening distance (mm)")
plt.plot(muscle_force, opening_distance)
plt.axvline(x = 0.17, color = 'r', ls='dashed', label = 'axvline - full height')
plt.xlim(1.1, -0.1)
plt.grid()


# plot opening distance by muscle activation

df_full = pd.read_csv("data_files/openingDistanceFull.txt", delim_whitespace=True, header=None,
    names = ['time', 'dist'])
df_half = pd.read_csv("data_files/openingDistanceHalf.txt", delim_whitespace=True, header=None,
    names = ['time', 'dist'])
df_ten_percent = pd.read_csv("data_files/openingDistanceTenPercent.txt", delim_whitespace=True, header=None,
    names = ['time', 'dist'])
df_five_percent = pd.read_csv("data_files/openingDistanceFivePercent.txt", delim_whitespace=True, header=None,
    names = ['time', 'dist'])
df_one_percent = pd.read_csv("data_files/openingDistanceOnePercent.txt", delim_whitespace=True, header=None,
    names = ['time', 'dist'])
df_point_five_percent = pd.read_csv("data_files/openingDistancePointFivePercent.txt", delim_whitespace=True, header=None,
    names = ['time', 'dist'])

x = [0.005*i for i in range(201)] # x axis as time in seconds

plt.subplot(1,2,2)

#fig = plt.figure()
#plt.title("")
plt.xlabel("Muscle activation")
plt.ylabel("Mouth opening distance (mm)")
plt.plot(x, df_full['dist'], label="100% muscle force")
plt.plot(x, df_half['dist'], label="50% muscle force")
plt.plot(x, df_ten_percent['dist'], label="10% muscle force")
plt.plot(x, df_five_percent['dist'], label="5% muscle force")
plt.plot(x, df_one_percent['dist'], label="1% muscle force")
#plt.plot(x, df_point_five_percent['dist'], label="0.5% muscle force")
plt.legend()
#plt.axis("equal")
plt.grid()
plt.show()

# reduced muscle force

# data for bite force at 10mm opening
x = [1.0-i*0.1 for i in range(10)]
x.append(0.05)
y = [651.47, 587.05, 505.03, 433.07, 362.76, 294.69, 229.36, 167, 107.75, 51.7, 24.85]

# data for bite force at 15mm opening
x2 = [1.0-i*0.1 for i in range(7)]
x2.append(0.1)
y2 = [618.05, 532.29, 448.70, 369.95, 297.82, 232.88, 174.94, 27.85]

# data for bite force at 5mm opening
x3 = [1.0, 0.7, 0.5, 0.3, 0.1]
y3 = [665.41, 461.07, 325.67, 192.51, 62.37]

fig = plt.figure()
#plt.title("")
plt.xlabel("Percentage of maximum muscle force")
plt.ylabel("Maxium bite force (N)")
plt.plot(x3, y3, label="at 5mm opening")
plt.plot(x, y, label="at 10mm opening")
plt.plot(x2, y2, label="at 15mm opening")
plt.legend()
plt.xlim(1.1, 0.0)
plt.grid()
plt.show()
