import matplotlib.pyplot as plt
import kinematic_model as km
import pandas as pd
import numpy as np
import math as m
from scipy.spatial.distance import euclidean

plt.rcParams.update({'font.size': 14})


## this script plots several figures:
## the trajectory of the lower incisors (during opening/chewing)
## the pose of the instantaneous frame (translation and rpy rotation),
## and torques for applying a certain force at the incisors during the movement


# data frames containing simulation data: IP displacement, instantaneous frame translation and rotation,
# and sample torque values for unit forces in the coordinate axes of the mandible coordinate frame
# torque Fy_x is the torque in the x axis for producing a force of (0 1 0) at the IP
# data frame for opening:
df_opening = pd.read_csv("data_files/MIPoseMouthOpening.txt", delim_whitespace=True, header=None,
    names = ['time', 'ip_x', 'ip_y', 'ip_z', 'transl_x', 'transl_y', 'transl_z', 'rot_x', 'rot_y', 'rot_z',
    'torqueFx_x', 'torqueFx_y', 'torqueFx_z', 'torqueFy_x', 'torqueFy_y', 'torqueFy_z', 'torqueFz_x', 'torqueFz_y', 'torqueFz_z'])
# data frame for chewing:
df_chewing = pd.read_csv("data_files/MIPoseMastication.txt", delim_whitespace=True, header=None,
    names = ['time', 'ip_x', 'ip_y', 'ip_z', 'transl_x', 'transl_y', 'transl_z', 'rot_x', 'rot_y', 'rot_z',
    'torqueFx_x', 'torqueFx_y', 'torqueFx_z', 'torqueFy_x', 'torqueFy_y', 'torqueFy_z', 'torqueFz_x', 'torqueFz_y', 'torqueFz_z'])

flagOpening = True # False for chewing

df = (df_opening if flagOpening else df_chewing)


# array for storing values of q
q_trajectory = []
# array for storing torques
torquesAxes = [[] for _ in range(3)] # torque for f in x, y, and z direction

# iterate over the rows of the dataframe
for i, row in df.iterrows():
    inc_target = [-row['ip_y'], row['ip_x'], row['ip_z'], 1]
    # calculate model inverse kinematics for incisor trajectory
    q = km.inverse_kinematics(inc_target)
    # set new initial q for optimisation
    km.set_q_init(q)
    q_trajectory.append(q)

    # iterate over x, y, z direction
    for i in range(3):
        f = np.array([0, 0, 0])
        f[i] = 1
        tx = km.forces_to_torques(q[3], q[4], q[5], f[0], f[1], f[2], True)
        torquesAxes[i].append(tx)

q_trajectory = np.array(q_trajectory)

### error calculation ###

# calculate the difference between instantaneous frame in simulation and kinematic model
# for rotation:
y = np.transpose(np.array([np.negative(df['rot_y'].values), df['rot_x'].values, df['rot_z'].values]))

errors = []
for i in range(len(y)):
    e = euclidean(y[i], q_trajectory[:, 3:6][i])
    errors.append(e)

#print("average error in rotation: " + str(1/len(y)*sum(errors)) + " deg")
#print("maximum error: " + str(max(errors)) + " deg")

# for translation:
y = np.transpose(np.array([np.negative(df['transl_y'].values), df['transl_x'].values, df['transl_z'].values]))

errors = []
for i in range(len(y)):
    e = euclidean(y[i], q_trajectory[:, 0:3][i])
    errors.append(e)

#print("average error in translation: " + str(1/len(y)*sum(errors)) + " mm")
#print("maximum error: " + str(max(errors)) + " mm")


## first plot: incisor trajectory ##

fig = plt.figure()
plt.axis('equal')
plt.ylabel("Z (mm)")
if flagOpening:
    #plt.title("incisor trajectory") # during mouth opening in saggital plane
    plt.plot(np.negative(df['ip_y']), df['ip_z'], c='r')
    plt.xlabel("X (mm)")
    plt.scatter(-df['ip_y'][0], df['ip_z'][0], c='b') # plot starting point
else:
    #plt.title("incisor trajectory") # during chewing in frontal plane
    plt.plot(df['ip_x'], df['ip_z'], c='r')
    plt.xlabel("Y (mm)")
    plt.scatter(df['ip_x'][0], df['ip_z'][0], c='b') # plot starting point
plt.show()

## second plot: translation and rotation of incisor frame ##

fig = plt.figure()
plt.subplot(1, 2, 1)
plt.title("Frame translation")
plt.xlabel("X (mm)")
plt.ylabel("Z (mm)")
plt.axis('equal')
plt.scatter(-df['transl_y'][0], df['transl_z'][0], c='b') # plot starting point
plt.plot(np.negative(df['transl_y']), df['transl_z'], c='r', label="artisynth")
plt.plot(q_trajectory[:, 0], q_trajectory[:, 2], c='g', label="kinematic model")
plt.legend()

plt.subplot(1, 2, 2)
plt.title("Frame rotation")
plt.xlabel("Time (s)")

if flagOpening:
    plt.plot(df['time'], df['rot_x'], c='r')
    plt.plot(df['time'], q_trajectory[:, 4], c='g')
    plt.ylabel("Pitch(y)")
else:
    plt.plot(df['time'], df['rot_y'], c='r', label="roll (x)")
    plt.plot(df['time'], df['rot_x'], c='r', ls=('dashed'), label="pitch (y)", linewidth=2)
    plt.plot(df['time'], df['rot_z'], c='r', ls=('dotted'), label="yaw (z)")
    plt.plot(df['time'], -q_trajectory[:, 3], c='g', label="roll (x)")
    plt.plot(df['time'], q_trajectory[:, 4], c='g', ls=('dashed'), label="pitch (y)")
    plt.plot(df['time'], q_trajectory[:, 5], c='g', ls=('dotted'), label="yaw (z)")
    plt.ylabel("Angle (deg)")
    plt.legend()

plt.show()

## third plot: torques ##

tx = np.array(torquesAxes[0])
ty = np.array(torquesAxes[1])
tz = np.array(torquesAxes[2])

fig = plt.figure()

plt.subplot(1, 3, 1)
plt.title("Torque for f=100")
plt.xlabel("Time (s)")
plt.xlim(-0.1, 1.1)
if flagOpening:
    plt.ylabel("Torque in y (Nmm)")
    plt.plot(df['time'], df['torqueFx_x'], c='r', label="artisynth")
    plt.plot(df['time'], tx[:, 1], c='g', label="kinematic_model")
else:
    plt.ylabel("Torque (Nmm)")
    plt.plot(df['time'], -df['torqueFx_y'], c='r', label="in x")
    plt.plot(df['time'], df['torqueFx_x'], c='r', ls=('dashed'), label="in y")
    plt.plot(df['time'], df['torqueFx_z'], c='r', ls=('dotted'), label="in z")
    plt.plot(df['time'], tx[:, 0], c='g', label="in x")
    plt.plot(df['time'], tx[:, 1], c='g', ls=('dashed'), label="in y")
    plt.plot(df['time'], tx[:, 2], c='g', ls=('dotted'), label="in z")


plt.subplot(1, 3, 2)
plt.title("Torque for f=010")
plt.xlabel("Time (s)")
plt.xlim(-0.1, 1.1)
if flagOpening:
    plt.ylabel("Torque in z (Nmm)")
    plt.axis("equal")
    plt.plot(df['time'], df['torqueFy_z'], c='r', label="artisynth")
    plt.plot(df['time'], ty[:, 2], c='g', label="kinematic_model")
else:
    plt.ylabel("Torque (Nmm)")
    plt.plot(df['time'], -df['torqueFy_y'], c='r', label="in x")
    plt.plot(df['time'], df['torqueFy_x'], c='r', ls=('dashed'), label="in y")
    plt.plot(df['time'], df['torqueFy_z'], c='r', ls=('dotted'), label="in z")
    plt.plot(df['time'], ty[:, 0], c='g', label="in x")
    plt.plot(df['time'], ty[:, 1], c='g', ls=('dashed'), label="in y")
    plt.plot(df['time'], ty[:, 2], c='g', ls=('dotted'), label="in z")


plt.subplot(1, 3, 3)
plt.title("Torque for f=001")
plt.xlabel("Time (s)")
plt.xlim(-0.1, 1.1)
if flagOpening:
    plt.ylabel("Torque in y (Nmm)")
    plt.plot(df['time'], df['torqueFz_x'], c='r', label="artisynth")
    plt.plot(df['time'], tz[:, 1], c='g', label="kinematic_model")
else:
    plt.ylabel("Torque (Nmm)")
    plt.plot(df['time'], -df['torqueFz_y'], c='r', label="in x")
    plt.plot(df['time'], df['torqueFz_x'], c='r', ls=('dashed'), label="in y")
    plt.plot(df['time'], df['torqueFz_z'], c='r', ls=('dotted'), label="in z")
    plt.plot(df['time'],tz[:, 0], c='g', label="in x")
    plt.plot(df['time'], tz[:, 1], c='g', ls=('dashed'), label="in y")
    plt.plot(df['time'], tz[:, 2], c='g', ls=('dotted'), label="in z")
plt.legend()
plt.show()
