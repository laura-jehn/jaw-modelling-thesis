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

## Simulation of the jaw

A model of the jaw is defined in `JawModel.java`, while `JawDemo.java` instantiates this model and implements the dynamics of the simulation. All Java source files for the jaw model can be found on the path `artisynth_models/src/artisynth/models/dynjaw/`.

### Running a custom simulation in ArtiSynth

For modifying the simulation, you can either edit `JawDemo.java` or, preferably, create a new class extending the `JawDemo` class. For demonstration purposes, let's call this class `MyJawDemo`.

#### Mouth opening simulation

For performing a mouth opening movement, you can run `MyJawDemo` and manually activate the opening muscles in a corresponding panel of the GUI. Or, you can incrementally activate the opening muscle in the advance() method of `MyJawDemo`. They can be decremented again in the same way, for performing a closing movement. Similarly, a laterotrusion movement can be produced by incrementing the inferior pterygoid on one side (`axialSprings/lip:excitation`) instead of the opening muscles.

```java
public StepAdjustment advance (double t0, double t1, int flags) {

   double openers_excitation = (double) myJawModel.getProperty ("exciters/bi_open:excitation").get ();
   if(openers_excitation < 1.0) {
      myJawModel.getProperty ("exciters/bi_open:excitation").set (openers_excitation+0.005);
   }
      
   StepAdjustment sa = super.advance (t0, t1, flags);
   return sa;
}
```

#### Chewing simulation

For simulating a chewing movement, in the attach() method of `MyJawDemo`, set the working directory to `data/controlchew` and set the file containing the input probes as `rightchew.art`. This will load the muscle activations for the chewing movement.

```java
public void attach(DriverInterface driver) {
   workingDirname = "data/controlchew";
   probesFilename = "rightchew.art";

   super.attach(driver);
}
```

#### Simulation of a therapy routine

For executing existing therapy routines, you can run the classes `TrajectoryFollowing` and `ResistanceTraining`. In `TrajectoryFollowing`, you can adjust the control parameters Kv and Kp, and provide a trajectory for the lower incisor point (IP) to be followed. In `ResistanceTraining` you can set the TrainingType (as opening, or left/right laterotrusion), as well as the increment of the resistance.

### Modifying the jaw model

The following modifications can be made on the jaw model (in `JawModel.java`):

* Set the condylar slope to one of the predefined slopes
  * Change the variable condylarSlopeType
* Set maximum mouth opening distance by adapting maximumMuscleForce of the opening muscles
* Set maximum bite force by adapting maximumMuscleForce of the closing muscles
  * Bite force can only be measured if there is a bolus between the teeth
  * The bolus is created in `JawDemo.java`, in line 437 the maximum resistance of the bolus can be set (for a continuous measurement of the bite force, the resistance should be high, otherwise the bolus will collapse and bite force will not be displayed)

### Exporting data from the simulation

During a simulation, you might want to save some data, like the incisor trace or the position of any other frame marker in the model. This can be done by running a simulation, and then, in the probe panel of the GUI, select "Export data" for the output probe of the data you want to save. Alternatively, you can run a script (see `saveMarkerPositions.py`). This is especially useful if there is no defined output probe for the data you want to save.

## Run python

For running the python scripts, you should have python version 3 installed. The main script is `python_scripts/kinematic_model.py`, whereas the other scripts are mainly for plotting.

### The kinematic model

The forward kinematics for a set of transformation parameters can be calculated in two ways. `forward_kinematics_4DOF()` gives the transformation matrix for x, y, beta and gamma, where alpha and z are determined internally, so that the position of the condyles remains on the condylar slope. `forward_kinematics_6DOF()` gives the transformation matrix when all six parameters are given, and also returns the distances of the condyles to the condylar slope, i.e. the error of the transformation.

```python
# IP is the incisor position, mTi is the corresponding transformation matrix
mTi, IP = forward_kinematics_4DOF(x, y, beta, gamma)
# rz1, rz2 describe how far the position of the condyles deviates from the condylar slope
mTi, rz1, rz2 = forward_kinematics_6DOF(x, y, z, alpha, beta, gamma):
```

The inverse kinematics can be used for determining the transformation parameters for a target IP position as follows:

```python
q = inverse_kinematics(IP_target)
```

Using the solution of the inverse kinematics for a target IP position, torques in the three rotation axes can be calculated for applying a force F at the incisors:

```python
# q[3:6] corresponds to alpha, beta and gamma
# True specifies that angles are in degrees
# F = (fx, fy, fz)
t = forces_to_torques(q[3], q[4], q[5], fx, fy, fz, True)
```

The last two steps can be iterated for a trajectory of the IP, which can be exported from the simulation for any movement (as described in a previous section). The calculation of forces to torques can be included when used in the context of a therapy routine, where, along with the IP trace, the applied forces (fx, fy, fz) are also given.

```python

# arrays for storing history of q and torques
q_trajectory = []
torque_trajectory = []

for IP_target in IP_trace:
   q = inverse_kinematics(IP_target)
   
   # set new initial q for optimisation
   set_q_init(q)
   q_trajectory.append(q)
   
   torque = forces_to_torques(q[3], q[4], q[5], fx, fy, fz, True)
   torque_trajectory.append(torque)
```

#### Personalising the kinematic model

The kinematic model can be personalised by
* defining a function s(x) for the condylar slope, and setting the slope variable of the model to this function
* changing the constraints for the transformation parameters in `inverse_kinematics()`.

## Contact
In case you have any questions about this project, feel free to contact me: laura.jehn@stud.tu-darmstadt.de.
