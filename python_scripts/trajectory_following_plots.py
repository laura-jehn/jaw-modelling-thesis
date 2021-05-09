from mpl_toolkits import mplot3d
import matplotlib.pyplot as plt

import pandas as pd
import numpy as np
import math as m

import kinematic_model as km

plt.rcParams.update({'font.size': 15})

df_15 = pd.read_csv("data_files/F_Kp15.txt", delim_whitespace=True, header=None,
    names = ['fx', 'fy', 'fz'])
df_30 = pd.read_csv("data_files/F_Kp30.txt", delim_whitespace=True, header=None,
    names = ['fx', 'fy', 'fz'])
df_20 = pd.read_csv("data_files/F_Kp20.txt", delim_whitespace=True, header=None,
    names = ['fx', 'fy', 'fz'])
df_10 = pd.read_csv("data_files/F_Kp10.txt", delim_whitespace=True, header=None,
    names = ['fx', 'fy', 'fz'])

## für Kp = 15, varied  Kv
df_0 = pd.read_csv("data_files/F_Kp15Kv0.txt", delim_whitespace=True, header=None,
    names = ['fx', 'fy', 'fz'])
df_005 = pd.read_csv("data_files/F_Kp15Kv005.txt", delim_whitespace=True, header=None,
    names = ['fx', 'fy', 'fz'])
df_002 = pd.read_csv("data_files/F_Kp15Kv002.txt", delim_whitespace=True, header=None,
    names = ['fx', 'fy', 'fz'])
df_001 = pd.read_csv("data_files/F_Kp15Kv001.txt", delim_whitespace=True, header=None,
    names = ['fx', 'fy', 'fz'])
df_0005 = pd.read_csv("data_files/F_Kp15Kv0005.txt", delim_whitespace=True, header=None,
    names = ['fx', 'fy', 'fz'])

IP = pd.read_csv("data_files/IPControlled.txt", delim_whitespace=True, header=None,
    names = ['time', 'ip_x', 'ip_y', 'ip_z'])


x = [i*0.001 for i in range(549)]

def plot_forces(df, k, label):
    plt.title("Forces for controller with " + label + "=" + str(k))
    plt.ylabel("Force (N)")
    plt.ylim(-5, 5)
    plt.plot(x, df['fx']/1000, label="x component")
    plt.plot(x, df['fy']/1000, label="y component")
    plt.plot(x, df['fz']/1000, label="z component")
    plt.legend()

# plots for different Kps
label = "Kp"
fig = plt.figure()
plt.subplot(1, 3, 1)
plot_forces(df_10, 10, label)
plt.subplot(1, 3, 2)
plot_forces(df_15, 15, label)
plt.subplot(1, 3, 3)
plot_forces(df_20, 20, label)
plt.xlabel("Time (s)")
plt.show()

# plots for different Kvs
label = "Kv"
fig = plt.figure()
fig.tight_layout(h_pad=20)
plt.subplot(2, 2, 1)
plot_forces(df_0, 0, label)
plt.subplot(2, 2, 2)
plot_forces(df_0005, 0.005, label)
plt.subplot(2, 2, 3)
plt.xlabel("Time (s)")
plot_forces(df_002, 0.02, label)
plt.subplot(2, 2, 4)
plt.xlabel("Time (s)")
plot_forces(df_005, 0.05, label)
plt.show()

# array for storing torques
torques = []

# iterate over the rows
for i, row in df_001.iterrows():
    inc_target = [-IP['ip_y'][i+1]+79.4085, IP['ip_x'][i+1], IP['ip_z'][i+1]-37.8728, 1]
    # calculate model inverse kinematics for incisor trajectory
    q = km.inverse_kinematics(inc_target)
    # set new initial q for optimisation
    km.set_q_init(q)
    tx = km.forces_to_torques(q[3], q[4], q[5], -row['fy']/1000, row['fx']/1000, row['fz']/1000, True)
    torques.append(tx)

torques = np.array(torques)

fig = plt.figure()
#plt.title("Torques for producing controller force trajectory")
plt.xlabel("Time (s)")
plt.ylabel("Torque (Nmm)")
plt.plot(x, torques[:,0], label="x component")
plt.plot(x, torques[:,1], label="y component")
plt.plot(x, torques[:,2], label="z component")
plt.legend()
plt.show()
