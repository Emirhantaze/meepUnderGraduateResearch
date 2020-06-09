import numpy as np
import matplotlib.pyplot as plt
def lorentzian(frequencyn=0, gamma=0 ,sigma=0,frequency=0):
    # frequencyn = frequencyn * 3e14
    return ((1/sigma)*(frequencyn**2))/((frequencyn**2)-(frequency**2)-(1j*frequency*gamma/(2*np.pi)))

def drude(frequencyn=0, gamma=0 ,sigma=0,frequency=0):
    frequencyn = frequencyn * 3e14  
    return(sigma*2*np.pi*1j*frequencyn)/(2*np.pi*frequency*(gamma-2*np.pi*frequency*1j))

um_scale = 1#3e14
eV_um_scale = um_scale/1.23984193
#------------------------------------------------------------------
# gold (Au)
# metal_range = mp.FreqRange(min=um_scale/6.1992, max=um_scale/.24797)
freqs = np.linspace(um_scale/1.2,um_scale/.4,100)

Au_plasma_frq = 9.03*eV_um_scale
Au_f0 = 0.760
Au_frq0 = 1e-10
Au_gam0 = 0.053*eV_um_scale
Au_sig0 = Au_f0*Au_plasma_frq**2/Au_frq0**2
Au_f1 = 0.024
Au_frq1 = 0.415*eV_um_scale      # 2.988 um
Au_gam1 = 0.241*eV_um_scale
Au_sig1 = Au_f1*Au_plasma_frq**2/Au_frq1**2
Au_f2 = 0.010
Au_frq2 = 0.830*eV_um_scale      # 1.494 um
Au_gam2 = 0.345*eV_um_scale
Au_sig2 = Au_f2*Au_plasma_frq**2/Au_frq2**2
Au_f3 = 0.071
Au_frq3 = 2.969*eV_um_scale      # 0.418 um
Au_gam3 = 0.870*eV_um_scale
Au_sig3 = Au_f3*Au_plasma_frq**2/Au_frq3**2
Au_f4 = 0.601
Au_frq4 = 4.304*eV_um_scale      # 0.288 um
Au_gam4 = 2.494*eV_um_scale
Au_sig4 = Au_f4*Au_plasma_frq**2/Au_frq4**2
Au_f5 = 4.384
Au_frq5 = 13.32*eV_um_scale      # 0.093 um
Au_gam5 = 2.214*eV_um_scale
Au_sig5 = Au_f5*Au_plasma_frq**2/Au_frq5**2

# Au_susc = [mp.DrudeSusceptibility(frequency=Au_frq0, gamma=Au_gam0, sigma=Au_sig0),
#            mp.LorentzianSusceptibility(frequency=Au_frq1, gamma=Au_gam1, sigma=Au_sig1),
#            mp.LorentzianSusceptibility(frequency=Au_frq2, gamma=Au_gam2, sigma=Au_sig2),
#            mp.LorentzianSusceptibility(frequency=Au_frq3, gamma=Au_gam3, sigma=Au_sig3),
#            mp.LorentzianSusceptibility(frequency=Au_frq4, gamma=Au_gam4, sigma=Au_sig4),
#            mp.LorentzianSusceptibility(frequency=Au_frq5, gamma=Au_gam5, sigma=Au_sig5)]
au=np.empty(100,dtype=np.cdouble)

for i in range(100):
    # au[i] = 1
    # au[i] += drude(Au_frq0,Au_gam0,Au_sig0,freqs[i])
    # au[i] += lorentzian(Au_frq1,Au_gam1,Au_sig1,freqs[i])
    # au[i] += lorentzian(Au_frq2,Au_gam2,Au_sig2,freqs[i])
    # au[i] += lorentzian(Au_frq3,Au_gam3,Au_sig3,freqs[i])
    # au[i] += lorentzian(Au_frq4,Au_gam4,Au_sig4,freqs[i])
    # au[i] += lorentzian(Au_frq5,Au_gam5,Au_sig5,freqs[i])
    au[i] = 2.25
    au[i] += lorentzian(1.1,1e-5,0.5,freqs[i])
    au[i] += lorentzian(0.5,0.1,2e-5,freqs[i])

plt.xlabel('wavelengths(umeter)')
plt.ylabel('dielectric')
plt.plot(1/freqs,np.real(au),color='r',label='real')
plt.legend()
plt.show()
plt.xlabel('wavelengths')
plt.ylabel(' dielectric')
plt.plot(1/freqs,np.imag(au),color='b', label = 'imaginery')
plt.legend()
plt.show()