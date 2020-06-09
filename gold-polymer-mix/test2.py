import meep as mp
import numpy as np
freq = 2
freqs = np.array(freq)[np.newaxis, np.newaxis, np.newaxis]
diag = mp.Vector3(1,1,1)
offdiag = mp.Vector3()
a = np.expand_dims(mp.Matrix(diag=diag,offdiag=offdiag),axis=0)
# print(a)
# print(freqs)
um_scale = 1
eV_um_scale = um_scale/1.23984193
Au_plasma_frq = 9.03*eV_um_scale
Au_f3 = 0.071
Au_frq3 = 2.969*eV_um_scale      # 0.418 um
Au_gam3 = 0.870*eV_um_scale
Au_sig3 = Au_f3*Au_plasma_frq**2/Au_frq3**2
c = mp.LorentzianSusceptibility(frequency=Au_frq3, gamma=Au_gam3, sigma=Au_sig3)
d = c.eval_susceptibility(freqs)
print(d)
print(np.squeeze(d+a))
t = Au_frq3*Au_frq3 / (Au_frq3*Au_frq3 - freq*freq - 1j*Au_gam3*freq) * Au_sig3
print(t)