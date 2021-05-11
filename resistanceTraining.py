# ArtisynthScript: "resistanceTraining"

# load resistance training simulation
loadModel('artisynth.models.dynjaw.ResistanceTraining')
m = root()

trainingList = [m.TrainingType.OPENING, m.TrainingType.LEFT_LATEROTRUSION, m.TrainingType.RIGHT_LATEROTRUSION]
trainingDuration = 5

lowerincisor = find("models/jawmodel/frameMarkers/lowerincisor")

for t in trainingList:
    m.setTrainingType(t)
    force_output_f = 'python_scripts/data_files/force_' + t.getTrainingName() + '.txt'
    li_output_f =  'python_scripts/data_files/li_' + t.getTrainingName() + '.txt'
    force_output = open(force_output_f, 'w')
    li_output = open(li_output_f, 'w')
    # each time step, get incisor position and force acting on model
    while getTime()<trainingDuration:
        force_output.write(m.getForce() + "\n")
        li_output.write(lowerincisor.getPosition().toString() + '\n')
        step()
    m.reset()
    reset()
    force_output.close()
    li_output.close()

quit()
