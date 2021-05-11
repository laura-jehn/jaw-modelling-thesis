from mpl_toolkits import mplot3d
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import math as m

plt.rcParams.update({'font.size': 14})

### plot IP trace from ArtiSynth for the three approximated condylar slopes ###

tg = pd.read_csv("data_files/TGSlopeOpening.txt", delim_whitespace=True, header=None,
    names = ['time', 'x', 'y', 'z'])
rg = pd.read_csv("data_files/RGSlopeOpening.txt", delim_whitespace=True, header=None,
    names = ['time', 'x', 'y', 'z'])
cg = pd.read_csv("data_files/CGSlopeOpening.txt", delim_whitespace=True, header=None,
    names = ['time', 'x', 'y', 'z'])

fig = plt.figure()
#plt.title("incisor trajectory during opening in sagittal plane")
plt.xlabel("X displacement (mm)")
plt.ylabel("Z displacement (mm)")
plt.plot(cg['y'], cg['z'], label='CG')
plt.plot(rg['y'], rg['z'], label='RG')
plt.plot(tg['y'], tg['z'], label='TG')
plt.axis("equal")
plt.grid()
plt.legend()
plt.show()
