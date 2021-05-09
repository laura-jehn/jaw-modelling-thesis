# ArtisynthScript: "saveMarkerPositions"

loadModel('artisynth.models.dynjaw.<Class>') # substitute <Class> with class name of model

jawModel = find("models/jawmodel") # get jaw model

ltmj = find("models/jawmodel/frameMarkers/ltmj") # get model element
rtmj = find("models/jawmodel/frameMarkers/rtmj")
lowerIncisor = find("models/jawmodel/frameMarkers/lowerincisor")
upperIncisor = find("models/jawmodel/frameMarkers/upperincisor")

rCondyleTrace = open('data/rtmjTrace.txt', 'w')
lCondyleTrace = open('data/ltmjTrace.txt', 'w')
lowerIncisorTrace = open('data/liTrace.txt', 'w')

play() # start simulation

while getTime()<2: # stop after 2 seconds
    rCondyleTrace.write(rtmj.getPosition().toString() + '\n') # get rtmj position and write to file
    lCondyleTrace.write(ltmj.getPosition().toString() + '\n')
    lowerIncisorTrace.write(lowerIncisor.getPosition().toString() + '\n')
    step() # advance simulation by one time step

lCondyleTrace.close()
rCondyleTrace.close()
lowerIncisorTrace.close()

quit() # close simulation
