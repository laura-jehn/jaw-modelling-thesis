# ArtisynthScript: "trajectoryFollowing"

loadModel('artisynth.models.dynjaw.TrajectoryFollowing')
m = root()

Kv = [0, 0.005, 0.01, 0.02]

for kv in Kv:
    f_name = '../python_scripts/data_files/x_error_' + str(kv) + '.txt'
    out_error = open(f_name, 'w')
    m.setKv(kv)
    for kp in range(5, 31, 5):
        m.setKp(kp)
        while getTime()<0.55:
            t = getTime()
            while getTime() == t:
                step()
        err = m.getXError()
        out_error.write(str(kp) + " " + str(err) + "\n")
        m.resetXError()
        reset() # resets simulation
        print("run: "+ str(kp) + ", " + str(kv))
        print(err)
    out_error.close()

quit()
