# jaw-modelling-thesis

## Installation

You need to have ArtiSynth (www.artisynth.org) installed to run the
models in this repository. There are several ways to install ArtiSynth, for a spotless integration with this project, follow the steps below:

1. Clone this repository.
2. Make sure to fulfill all prerequisites listed in Chapter 2 of the [ArtiSynth Installation Guide](https://www.artisynth.org/manuals/index.jsp).
3. Install the Eclipse IDE. Installation help can be found in Chapter 12.
4. From GitHub, import the [artisynth_core](https://github.com/artisynth/artisynth_core.git) project into Eclipse, following Chapter 6.1. During this process, you will be asked to select a local destination for the project. **Set jaw-modelling-thesis/artisynth_core as the local destination.** This location will be the <ARTISYNTH_HOME> location from where all other files are referenced.
5. Make sure to run artisynth_core/bin/updateArtisynthLibs for downloading Java and native libraries for proper compilation of the project.

You should now have a running ArtiSynth installation. Next, you need to integrate the external models in this repository.

1. Import the artisynth_models directory into the eclipse workspace.
2. Right click on the "Run"-Button in Eclipse and select "Run Configurations".
3. Go to Java Application/ArtiSynth on the left side of the panel.
4. Go to "Dependencies", select "ClassPath" entries and click "Add projects", then add the artisynth_models project.

Steps 2-4 are explained in Chapter 12.6 of the Installation guide for an older version of Eclipse, where the names of the selections slightly differ.
The artisynth_models project should now have been added to the ArtiSynth launch configuration.

## Run ArtiSynth

1. Right click on the "Run"-Button in Eclipse, select "Run Configurations" and go to Java Application/ArtiSynth on the left side of the panel.
2. Put -model artisynth.models.dynjaw.\<Class\> as command line argument in tab "Arguments". For a simple Demo, substitute \<Class\> with JawDemo.java.
3. For running a script, put -noGui -script ../\<script_name\> as command line argument.

## Run python

For running the python scripts, you should have python version 3 installed.

## Making modifications

### Measuring bite force

In JawDemo.java, set bolus resistance.
