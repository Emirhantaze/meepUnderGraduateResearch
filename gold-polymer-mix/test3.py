import meep as mp
import numpy as np 
from meep.materials import Au
import matplotlib.pyplot as plt
import pandas as pd 
from functions import mixsolver
# default unit length is 1 um
df = pd.read_csv (r'./gold-polymer-mix/RefractiveIndexINFO.csv')
polimer = df['n'].to_numpy()**2
um_scale = 1.0

# conversion factor for eV to 1/um [=1/hc]
eV_um_scale = um_scale/1.23984193
var = np.linspace(1e-10,25,5)
metal_range = mp.FreqRange(min=um_scale/6.1992, max=um_scale/.24797)

Au_plasma_frq = 9.03*eV_um_scale
Au_f0 = 0.760
Au_frq0 = var[3]
Au_gam0 = 0.053*eV_um_scale
Au_sig0 = Au_f0*Au_plasma_frq**2/Au_frq0**2
Au_f1 = 0.024
Au_frq1 = var[0]*eV_um_scale      # 2.988 um
Au_gam1 = 0.241*eV_um_scale
Au_sig1 = Au_f1*Au_plasma_frq**2/Au_frq1**2
Au_f2 = 0.010
Au_frq2 = var[0]*eV_um_scale      # 1.494 um
Au_gam2 = 0.345*eV_um_scale
Au_sig2 = Au_f2*Au_plasma_frq**2/Au_frq2**2
Au_f3 = 0.071
Au_frq3 = var[0]*eV_um_scale      # 0.418 um
Au_gam3 = 0.870*eV_um_scale
Au_sig3 = Au_f3*Au_plasma_frq**2/Au_frq3**2
Au_f4 = 0.601
Au_frq4 = var[0]*eV_um_scale      # 0.288 um
Au_gam4 = 2.494*eV_um_scale
Au_sig4 = Au_f4*Au_plasma_frq**2/Au_frq4**2
Au_f5 = 4.384
Au_frq5 = var[4]*eV_um_scale      # 0.093 um
Au_gam5 = 2.214*eV_um_scale
Au_sig5 = Au_f5*Au_plasma_frq**2/Au_frq5**2

Au_susc = [mp.DrudeSusceptibility(frequency=Au_frq0, gamma=Au_gam0, sigma=Au_sig0),
           mp.LorentzianSusceptibility(frequency=Au_frq1, gamma=Au_gam1, sigma=Au_sig1),
           mp.LorentzianSusceptibility(frequency=Au_frq2, gamma=Au_gam2, sigma=Au_sig2),
           mp.LorentzianSusceptibility(frequency=Au_frq3, gamma=Au_gam3, sigma=Au_sig3),
           mp.LorentzianSusceptibility(frequency=Au_frq4, gamma=Au_gam4, sigma=Au_sig4),
           mp.LorentzianSusceptibility(frequency=Au_frq5, gamma=Au_gam5, sigma=Au_sig5)]

Auour = mp.Medium(epsilon=1.0, E_susceptibilities=Au_susc, valid_freq_range=metal_range)
freqs = np.linspace(um_scale/0.7,um_scale/0.35,101)
au = np.empty(101,dtype=np.cdouble)
freqs = np.linspace(um_scale/0.7,um_scale/0.35,101)
au = np.empty(101,dtype=np.cdouble)
auour = np.empty(101,dtype=np.cdouble)
for i in range (101):
    auour[i]= Auour.epsilon(freqs[i])[1][1]
    au[i]= Au.epsilon(freqs[i])[1][1]
mix1 = np.empty(101,dtype=np.cdouble)
mix2 = np.empty(101,dtype=np.cdouble)

for i in range(101):
    temp = np.roots(mixsolver(0.5,au[i],polimer[i]))
    mix1[i] = temp[0]
    mix2[i] = temp[1]
mix1 = np.sqrt(mix1,dtype=np.cdouble)
auour = np.sqrt(auour,dtype=np.cdouble)
au = np.sqrt(au,dtype=np.cdouble)
plt.xlabel('wavelengths(umeter)')
plt.ylabel('refractive index')
plt.plot(1/freqs,np.real(mix1),color='C1',label='real mix')
plt.plot(1/freqs,np.imag(mix1),color='C2', label = 'imaginery mix')
plt.plot(1/freqs,np.real(au),color='C3', label = 'real au')
plt.plot(1/freqs,np.imag(au),color='C4', label = 'imaginery au')
# plt.plot(1/freqs,np.real(auour),color='C3', label = 'real auour')
# plt.plot(1/freqs,np.imag(auour),color='C4', label = 'imaginery auour')
# plt.plot(1/freqs,np.sqrt(polimer),color='C5', label = 'real polimer')

plt.legend()
plt.show()