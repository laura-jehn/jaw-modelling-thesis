from mpl_toolkits import mplot3d
import matplotlib.pyplot as plt
import math

plt.rcParams.update({'font.size': 14})

start=4
end=20

#fig = plt.figure()
#for i in range(start, end, 2):
    #f_name = "trajectory" + str(i)
    #trajectories = [[],[],[],[],[],[]]
    #x_ist = []
    #y_ist = []
    #z_ist = []
    #x_soll = []
    #y_soll = []
    #z_soll = []

    #with open(f_name, "r") as f:
    #    for l in f:
    #        l= l.strip()
    #        points = l.split(" ")[1:]
    #        [trajectories[x].append(float(points[x])) for x in range(len(points))]

    #ax = fig.add_subplot(4, 4, int((i-start+100)/100.0), projection='3d')
    #ax.plot(trajectories[0], trajectories[1], trajectories[2], c='r', label='x_ist')
    #ax.plot(trajectories[3], trajectories[4], trajectories[5], c='b', label='x_soll')
    #ax.legend()
    #plt.title("magnitude " + str(i))
    #plt.xlabel("x")
    #plt.ylabel("y")

#plt.show()

Kv = [0, 0.005, 0.01, 0.02]

fig = plt.figure()
#plt.title("")
plt.xlabel("Kp")
plt.ylabel("RMSE")

for kv in Kv:
    f = open("data_files/x_error_" + str(kv) + ".txt", "r")
    lines = f.readlines()
    i = []
    err = []

    for l in lines:
        p = l.split(' ')
        i.append(float(p[0]))
        err.append(math.sqrt(float(p[1])))

    f.close()
    plt.plot(i, err, label="Kv = " + str(kv))

#plt.axis('')
plt.ylim(0, 10)
plt.legend()
plt.show()
