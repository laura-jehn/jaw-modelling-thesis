import matplotlib.pyplot as plt
import kinematic_model as km
import pandas as pd

plt.rcParams.update({'font.size': 14})

# data frame for a limited chewing movement
df = pd.read_csv("data_files/incisorDispReducedChewing.txt", delim_whitespace=True, header=None,
    names = ['ip_x', 'ip_y', 'ip_z'])

# data frame for normal chewing movement
df_2 = pd.read_csv("data_files/chewingTrajectory.txt", delim_whitespace=True, header=None,
    names = ['time', 'ip_x', 'ip_y', 'ip_z'])

# data frame for the controlled chewing movement
df_3 = pd.read_csv("data_files/incisorDispControlled.txt", delim_whitespace=True, header=None,
    names = ['time', 'ip_x', 'ip_y', 'ip_z'])

## incisor trajectory during chewing in frontal plane ##

fig = plt.figure()
plt.plot(df_2['ip_x'][:-55], df_2['ip_z'][:-55], label="desired IP trajectory")
plt.plot(df['ip_x'], df['ip_z'], label="with compromised muscle function")
plt.plot(df_3['ip_x'], df_3['ip_z'], label="with controller")
plt.xlabel("Y (mm)")
plt.ylabel("Z (mm)")
plt.axis('equal')
plt.legend()
annotation_times = [150, 400, 500]
for at in annotation_times:
    plt.annotate("", xytext=(df_2['ip_x'][at],df_2['ip_z'][at]),xy=(df_2['ip_x'][at+10],df_2['ip_z'][at+10]),
    arrowprops=dict(arrowstyle="->", color='b'), size = 30)
plt.scatter(df['ip_x'][0], df['ip_z'][0], c='r') # plot starting point
plt.show()
