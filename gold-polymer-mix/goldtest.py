import matplotlib.pyplot as plt
import pandas as pd
from meep.materials import Au, Au_visible
import numpy as np
df = pd.read_csv(r'./gold-polymer-mix/pdms.csv')
polimer = df['n'].to_numpy()**2
f = df['Wavelength, µm'].to_numpy()


df = pd.read_csv(r'./gold-polymer-mix/goldMcPeak2015.csv')
w = df['Wavelength, µm'].to_numpy()
n = df['n'].to_numpy()
k = df['k'].to_numpy()
auorj = (n + k*1j)**2
au = Au_visible.epsilon(1/w)[:, 0, 0]

plt.plot(w, np.real(auorj), color='C1', label='Refractiveindexinfo gold real')
plt.plot(w, np.imag(auorj), color='C2', label='Refractiveindexinfo gold imag')
plt.plot(w, np.real(au), color='C3', label='Meep gold real')
plt.plot(w, np.imag(au), color='C4', label='Meep gold imag')
plt.xlabel('Wavelengths  µm ')
plt.ylabel('Epsilon')
plt.title("Meep vs Refractiveindex.info gold epsilon")
plt.legend()
plt.grid()
plt.show()
