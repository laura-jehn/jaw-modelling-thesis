# ArtisynthScript: "resistanceTraining"

loadModel('artisynth.models.dynjaw.ResistanceTraining')
m = root()

trainingList = [m.TrainingType.OPENING, m.TrainingType.LEFT_LATEROTRUSION, m.TrainingType.RIGHT_LATEROTRUSION]
trainingDuration = 5

lowerincisor = find("models/jawmodel/frameMarkers/lowerincisor")

for i in range(1): #len(trainingList)
    t = trainingList[i]
    m.setTrainingType(t)
    force_output_f = '../python_scripts/data_files/force_' + t.getTrainingName() + '_mediumMuscleActivation.txt'
    li_output_f =  '../python_scripts/data_files/li_' + t.getTrainingName() + '_mediumMuscleActivation.txt'
    force_output = open(force_output_f, 'w')
    li_output = open(li_output_f, 'w')
    while getTime()<trainingDuration:
        force_output.write(m.getForce() + "\n")
        li_output.write(lowerincisor.getPosition().toString() + '\n')
        step()
    m.reset()
    reset()
    force_output.close()
    li_output.close()

quit()
