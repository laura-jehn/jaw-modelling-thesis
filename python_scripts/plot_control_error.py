from mpl_toolkits import mplot3d
import matplotlib.pyplot as plt
import math

plt.rcParams.update({'font.size': 14})

### plots controller error for different values of Kv and Kp

Kv = [0, 0.005, 0.01, 0.02]

fig = plt.figure()
#plt.title("")
plt.xlabel("Kp")
plt.ylabel("RMSE (mm)")

for kv in Kv:
    f = open("data_files/x_error_" + str(kv) + ".txt", "r")
    lines = f.readlines()
    i = []
    err = []

    for l in lines:
        p = l.split(' ')
        i.append(float(p[0]))
        err.append(math.sqrt(float(p[1])/500))

    f.close()
    plt.plot(i, err, label="Kv = " + str(kv))

plt.ylim(0, 0.5)
plt.legend()
plt.show()
