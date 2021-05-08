# jaw-modelling-thesis

This project was developed in the scope of a bachelor thesis at the TU Darmstadt (Department of Simulation, System Optimisation and Robotics). The aim of the thesis was to work out methods for personalising an existing jaw model and develop a framework for an advanced jaw rehabilitation device, which will allow the development of personalised treatment strategies for patients suffering from temporomandibular disorders (TMD).

The `artisynth_models/` directory in this project is an adaptation of the [artisynth_models](https://github.com/artisynth/artisynth_models.git) project. It contains a biomechanical jaw model, to which some personalisations were added, and simulations of developed therapy routines on the model. The top-level python scripts are ArtiSynth scripts, using Jython for interfacing the ArtiSynth simulation. The `python_scripts/` directory contains the developed kinematic model for the orthosis framework, and all data files and scripts used for plotting.

## Installation

You need to have ArtiSynth (www.artisynth.org) installed to run the
models in this repository. There are several ways to install ArtiSynth, for a spotless integration with this project, follow the steps below:

1. Clone this repository in a location of your choice.
2. Go to the [ArtiSynth Installation Guide](https://www.artisynth.org/manuals/index.jsp) for your operating system.
3. Make sure to fulfill all prerequisites listed in Chapter 2.
4. Install the Eclipse IDE. Installation help can be found in Chapter 12.
5. From GitHub, import the [artisynth_core](https://github.com/artisynth/artisynth_core.git) project into Eclipse, following Chapter 6.1. During this process, you will be asked to select a local destination for the project. **Set jaw-modelling-thesis/artisynth_core as the local destination.** This location will be the <ARTISYNTH_HOME> location from where all other files are referenced.
6. Make sure to run artisynth_core/bin/updateArtisynthLibs for downloading Java and native libraries for proper compilation of the project.

You should now have a running ArtiSynth installation. Next, you need to integrate the external models in this repository.

1. Import the artisynth_models directory into the eclipse workspace (Import > General > Existing Projects into Workspace).
2. Right click on the "Run"-Button in Eclipse and select "Run Configurations".
3. Go to Java Application/ArtiSynth on the left side of the panel.
4. Go to "Dependencies", select "ClassPath" entries and click "Add projects", then add the artisynth_models project.

Steps 2-4 are explained in Chapter 12.6 of the Installation guide for an older version of Eclipse, where the names of the selections differ slightly.
The artisynth_models project should now have been added to the ArtiSynth launch configuration.

## Run ArtiSynth

1. Right click on the "Run"-Button in Eclipse, select "Run Configurations" and go to Java Application/ArtiSynth on the left side of the panel.
2. Put -model artisynth.models.dynjaw.\<Class\> as command line argument in tab "Arguments". For a simple Demo, substitute \<Class\> with JawDemo. Then, run the simulation.
3. For running the simulation with a script, put -noGui -script ../\<script_name\> as command line argument.

## Run python

For running the python scripts, you should have python version 3 installed. The main script is `python_scripts/kinematic_model.py`, and `python_scripts/kinematic_model_evaluation.py` contains examples for using the kinematic model. The other scripts are mainly for plotting.

*TODO: add example for using the kinematic model

## Making modifications

### Running a custom simulation in ArtiSynth

In JawDemo.java, set bolus resistance.

# Contact
In case you have any questions about this project, feel free to contact me: laura.jehn@stud.tu-darmstadt.de.
