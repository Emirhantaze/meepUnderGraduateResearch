import numpy as np
import pandas as pd
from functions import calcdrude, calclorentizan, mixsolver
import matplotlib.pyplot as plt
from numpy import load

df = pd.read_csv(r'./gold-polymer-mix/goldMcPeak2015.csv')
w = df['Wavelength, µm'].to_numpy()
n = df['n'].to_numpy()
k = df['k'].to_numpy()
auorj = (n + k*1j)**2
f = 1/w

df = pd.read_csv(r'./gold-polymer-mix/SilverMcPeak2015.csv')
w = df['Wavelength, µm'].to_numpy()
n = df['n'].to_numpy()
k = df['k'].to_numpy()
agorj = (n + k*1j)**2
f = 1/w

um_scale = 1.0
# conversion factor for eV to 1/um [=1/hc]
eV_um_scale = um_scale/1.23984193

polimer = np.empty(len(f), dtype=np.cdouble)
x = [0.00555007,  0.5687775, -0.40683289,  1.39844407,  4.66929214]
polimer = (x[0]*x[4]**((x[1]/w)+x[2])) + x[3]
polimer = polimer**2
mix1 = mixsolver([0.25, 0.45, 0.30], auorj, agorj, polimer)
mix1 = mix1**0.5

ts1 = 2/(1+mix1)
ts2 = 2*mix1/(1+mix1)
bx = 0.02*1e-6
k = 2*np.pi/(w*1e-6)
y = 1 + np.exp(-k*mix1.imag*bx)

plt.plot(w, y)
y = 1 + np.exp(-k*mix1.imag*bx)*(ts1**2)*(ts2**2)
# plt.plot(mix1.imag)
plt.plot(w, y)

plt.show()
