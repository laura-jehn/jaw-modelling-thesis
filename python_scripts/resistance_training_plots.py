from mpl_toolkits import mplot3d
import matplotlib.pyplot as plt

import pandas as pd
import numpy as np
import math as m

import kinematic_model as km

plt.rcParams.update({'font.size': 14})

trainingList = ['opening', 'llat', 'rlat']

x = [i*0.005 for i in range(1000)] # x axis values (time in seconds)

for t in trainingList:
    name = t
    force = pd.read_csv("data_files/force_" + name + ".txt", delim_whitespace=True, header=None,
        names = ['fx', 'fy', 'fz'])
    li = pd.read_csv("data_files/li_" + name + ".txt", delim_whitespace=True, header=None,
        names = ['ip_x', 'ip_y', 'ip_z'])

    fig = plt.figure()
    plt.subplot(1, 2, 1)

    if name == 'opening':
        plt.title("Force in z")
        df_fullMuscleForce = pd.read_csv("data_files/force_" + name + "_fullMuscleForce.txt", delim_whitespace=True, header=None,
            names = ['fx', 'fy', 'fz'])
        df_mediumMuscleActivation = pd.read_csv("data_files/force_" + name + "_mediumMuscleActivation.txt", delim_whitespace=True, header=None,
            names = ['fx', 'fy', 'fz'])
        z = True
        plt.plot(x, force['fz']/1000, label='with compromised muscles')
        plt.plot(x, df_fullMuscleForce['fz']/1000, label='with full muscle force', ls='dashed', c='r')
        plt.plot(x, df_mediumMuscleActivation['fz']/1000, label='with 50% muscle activation', ls='dotted', c='r')
    else:
        plt.title("Force in x")
        plt.plot(x, force['fx']/1000)
        z = False

    #plt.title(name)
    plt.xlabel("Time (s)")
    plt.ylabel("Force (N)")
    plt.legend()

    # array for storing torques
    torques = []

    # iterate over the rows
    for i, row in force.iterrows():
        inc_target = [-(li['ip_y'][i]+47.9584)+79.4085, li['ip_x'][i], li['ip_z'][i]-41.7642-37.8728, 1]
        # calculate model inverse kinematics for incisor trajectory
        q = km.inverse_kinematics(inc_target)
        # set new initial q for optimisation
        km.set_q_init(q)
        if z:
            tx = km.forces_to_torques(q[3], q[4], q[5], 0, 0, row['fz']/1000, True)
        else:
            tx = km.forces_to_torques(q[3], q[4], q[5], 0, row['fx']/1000, 0, True)
        torques.append(tx)

    torques = np.array(torques)

    plt.subplot(1, 2, 2)
    plt.title("Torques for forces with compromised muscle function")
    plt.xlabel("Time (s)")
    plt.ylabel("Torque (Nmm)")
    plt.plot(x, torques[:,0], label="in x axis")
    plt.plot(x, torques[:,1], label="in y axis")
    plt.plot(x, torques[:,2], label="in z axis")
    plt.legend()
    plt.show()
