# jaw-modelling-thesis

### ArtiSynth Installation

1. Download the repository via GitHub.
2. Install the Eclipse IDE and import the artisynth_core and artiynth_models projects from this repository. Installation of Eclipse for ArtiSynth is explained in [ArtiSynth Installation Guide](https://www.artisynth.org/Documentation/InstallGuide) (Chapter 12 - The Eclipse IDE). Make sure you fulfill all [system requirements](https://www.artisynth.org/doc/info) (Chapter 2 - Prerequisites).

### Run ArtiSynth

1. Right click on the "Run"-Button in Eclipse and select "Run Configurations".
2. Put -model artisynth.models.dynjaw.<Class> as command line argument. For a simple Demo, substitute <Class> with JawDemo.java.
3. For running a script, put -noGui -script scripts/<script_name> as command line argument.

### Run python

For running the python scripts, you should have python version 3 installed.

## Making modifications

### Measuring bite force

In JawDemo.java, set bolus resistance.
