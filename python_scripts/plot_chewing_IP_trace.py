import matplotlib.pyplot as plt
import kinematic_model as km
import pandas as pd

plt.rcParams.update({'font.size': 14})

# data frame for chewing
df = pd.read_csv("data_files/incisorDispReducedChewing.txt", delim_whitespace=True, header=None,
    names = ['ip_x', 'ip_y', 'ip_z'])

# data frame for chewing
df_2 = pd.read_csv("data_files/chewingTrajectory.txt", delim_whitespace=True, header=None,
    names = ['time', 'ip_x', 'ip_y', 'ip_z'])

df_3 = pd.read_csv("data_files/incisorDispControlled.txt", delim_whitespace=True, header=None,
    names = ['time', 'ip_x', 'ip_y', 'ip_z'])

#df_vel = pd.read_csv("../chewingTrajectoryWithVelocity.txt", delim_whitespace=True, header=None,
    #names = ['time', 'ip_x', 'ip_y', 'ip_z', 'vel_x', 'vel_y', 'vel_z'])

## incisor trajectory during chewing in frontal plane ##

fig = plt.figure()
plt.plot(df_2['ip_x'][:-55], df_2['ip_z'][:-55], label="desired IP trajectory")
plt.plot(df['ip_x'], df['ip_z'], label="with compromised muscle function")
plt.plot(df_3['ip_x'], df_3['ip_z'], label="with controller")
plt.xlabel("Y (mm)")
plt.ylabel("Z (mm)")
plt.axis('equal')
plt.legend()
plt.annotate("", xytext=(df_2['ip_x'][150],df_2['ip_z'][150]),xy=(df_2['ip_x'][160],df_2['ip_z'][160]),
    arrowprops=dict(arrowstyle="->", color='b'), size = 30)
plt.annotate("", xytext=(df_2['ip_x'][400],df_2['ip_z'][400]),xy=(df_2['ip_x'][410],df_2['ip_z'][410]),
    arrowprops=dict(arrowstyle="->", color='b'), size = 30)
plt.annotate("", xytext=(df_2['ip_x'][500],df_2['ip_z'][500]),xy=(df_2['ip_x'][510],df_2['ip_z'][510]),
    arrowprops=dict(arrowstyle="->", color='b'), size = 30)
# plot starting point
plt.scatter(df['ip_x'][0], df['ip_z'][0], c='r')
plt.show()

#x = [i*0.001 for i in range(df_vel.shape[0])]

#fig = plt.figure()
#plt.title("")
#plt.ylabel("Velocity (mm/s)")
#plt.xlabel("Time (s)")
#plt.plot(x, df_vel['vel_x'], label="x")
#plt.plot(x, df_vel['vel_y'], label="y")
#plt.plot(x, df_vel['vel_z'], label="z")
#plt.legend()
#plt.show()
