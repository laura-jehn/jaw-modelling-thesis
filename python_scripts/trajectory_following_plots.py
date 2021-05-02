from mpl_toolkits import mplot3d
import matplotlib.pyplot as plt

import pandas as pd
import numpy as np
import math as m

import kinematic_model as km

plt.rcParams.update({'font.size': 15})

#df_200 = pd.read_csv("../data/trajectoryF200.txt", delim_whitespace=True, header=None,
#    names = ['fx', 'fy', 'fz'])
df_15 = pd.read_csv("data_files/F_Kp15.txt", delim_whitespace=True, header=None,
    names = ['fx', 'fy', 'fz'])
df_30 = pd.read_csv("data_files/F_Kp30.txt", delim_whitespace=True, header=None,
    names = ['fx', 'fy', 'fz'])
df_20 = pd.read_csv("data_files/F_Kp20.txt", delim_whitespace=True, header=None,
    names = ['fx', 'fy', 'fz'])
df_10 = pd.read_csv("data_files/F_Kp10.txt", delim_whitespace=True, header=None,
    names = ['fx', 'fy', 'fz'])

## für Kp = 15, vary  Kv
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

#df_16 = pd.read_csv("data_files/F_Kp16.txt", delim_whitespace=True, header=None,
    #names = ['fx', 'fy', 'fz'])

IP = pd.read_csv("data_files/IPControlled.txt", delim_whitespace=True, header=None,
    names = ['time', 'ip_x', 'ip_y', 'ip_z'])


tf = 1
x = [i*0.001 for i in range(549-tf)]

def plot_forces(df, kp):
    plt.title("Forces for controller with Kp=" + str(kp))
    plt.ylabel("Force (N)")
    plt.ylim(-5, 5)
    plt.plot(x, df['fx'][:-tf]/1000, label="x component")
    plt.plot(x, df['fy'][:-tf]/1000, label="y component")
    plt.plot(x, df['fz'][:-tf]/1000, label="z component")
    plt.legend()

fig = plt.figure()
plt.subplot(1, 3, 1)
plot_forces(df_10, 10)
plt.subplot(1, 3, 2)
plot_forces(df_15, 15)
plt.subplot(1, 3, 3)
plot_forces(df_20, 20)
plt.xlabel("Time (s)")
plt.show()

fig = plt.figure()
fig.tight_layout(h_pad=20)
plt.subplot(2, 2, 1)
plot_forces(df_0, 0)
plt.subplot(2, 2, 2)
plot_forces(df_0005, 0.005)
plt.subplot(2, 2, 3)
plt.xlabel("Time (s)")
plot_forces(df_002, 0.02)
plt.subplot(2, 2, 4)
plt.xlabel("Time (s)")
plot_forces(df_005, 0.05)
plt.show()

# array for storing torques
torques = []

#print(IP.shape[0])
#print(df_200.shape[0])

# iterate over the rows
for i, row in df_001[:-tf].iterrows():
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
