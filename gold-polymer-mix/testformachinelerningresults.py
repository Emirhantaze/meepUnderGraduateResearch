import numpy as np
import scipy.optimize as opt
import pandas as pd
from functions import calcdrude, calclorentizan, mixsolver, predict_single, preprocess
import matplotlib.pyplot as plt
ORAN_AU = 0.1
ORAN_AG = 0.5
ORAN_P = 0.4
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

mix1 = mixsolver([ORAN_AU, ORAN_AG, ORAN_P], auorj, agorj, polimer)


def fun1(x):
    um_scale = 1.0
    # conversion factor for eV to 1/um [=1/hc]
    eV_um_scale = um_scale/1.23984193
    Au_plasma_frq = x[0]*eV_um_scale

    Au_f0 = x[1]
    Au_frq0 = 1e-10
    Au_gam0 = x[2]*eV_um_scale
    Au_sig0 = Au_f0*Au_plasma_frq**2/Au_frq0**2

    Au_f1 = x[3]
    Au_frq1 = x[4]    # 0.42 um
    Au_gam1 = x[5]*eV_um_scale
    Au_sig1 = Au_f1*Au_plasma_frq**2/Au_frq1**2

    Au_f2 = x[6]
    Au_frq2 = x[7]  # 0.42 um
    Au_gam2 = x[8]*eV_um_scale
    Au_sig2 = Au_f2*Au_plasma_frq**2/Au_frq2**2
    Au_f3 = x[9]
    Au_frq3 = x[10]*eV_um_scale      # 0.418 um
    Au_gam3 = x[11]*eV_um_scale
    Au_sig3 = Au_f3*Au_plasma_frq**2/Au_frq3**2
    Au_f4 = x[12]
    Au_frq4 = x[13]*eV_um_scale      # 0.288 um
    Au_gam4 = x[14]*eV_um_scale
    Au_sig4 = Au_f4*Au_plasma_frq**2/Au_frq4**2
    Au_f5 = x[15]
    Au_frq5 = x[16]*eV_um_scale      # 0.093 um
    Au_gam5 = x[17]*eV_um_scale
    Au_sig5 = Au_f5*Au_plasma_frq**2/Au_frq5**2
    fx = x[18] + calcdrude(frequency=f, frequencyn=Au_frq0,
                           sigma=Au_sig0, gamma=Au_gam0)
    fx = fx + calclorentizan(frequency=f, frequencyn=Au_frq1,
                             gamma=Au_gam1, sigma=Au_sig1)
    fx = fx + calclorentizan(frequency=f, frequencyn=Au_frq2,
                             gamma=Au_gam2, sigma=Au_sig2)
    fx = fx + calclorentizan(frequency=f, frequencyn=Au_frq3,
                             gamma=Au_gam3, sigma=Au_sig3)
    fx = fx + calclorentizan(frequency=f, frequencyn=Au_frq4,
                             gamma=Au_gam4, sigma=Au_sig4)
    fx = fx + calclorentizan(frequency=f, frequencyn=Au_frq5,
                             gamma=Au_gam5, sigma=Au_sig5)

    last = mix1-fx  # fx burada üreittiğimiz değerşler mix1 ise ulaşmaya çalıştığımız değerler
    # lasti = np.corrcoef(np.real(mix1),np.real(fx))[1][0]
    # lastr = np.corrcoef(np.imag(mix1),np.imag(fx))[1][0]
    # # https://en.wikipedia.org/wiki/Reduced_chi-squared_statistic
    # print ((np.sum((np.real(last)**2)+(np.imag(last)**2))+40-(20*lasti)-(20*lastr)) )
    x = ((np.sum(np.real(last)**2)/(0.001)) +
         (np.sum(np.imag(last)**2)/0.001))/(len(mix1)-1)
    # x burada fitting için kullandığımız ve azaltmaya çalıştığımız parametre
    # print(x)
    # return (np.sum((np.real(last)**2)+(np.imag(last)**2))+40-(20*lasti)-(20*lastr))
    assert x != np.nan, f'{x} is problematic'
    return x


machinelerningout = predict_single(np.flip(mix1))

print((machinelerningout))
val = machinelerningout
Au_plasma_frq = val[0]*eV_um_scale

Au_f0 = val[1]
Au_frq0 = 1e-10
Au_gam0 = val[2]*eV_um_scale
Au_sig0 = Au_f0*Au_plasma_frq**2/Au_frq0**2


Au_f1 = val[3]
Au_frq1 = val[4]    # 0.42 um
Au_gam1 = val[5]*eV_um_scale
Au_sig1 = Au_f1*Au_plasma_frq**2/Au_frq1**2

Au_f2 = val[6]
Au_frq2 = val[7]   # 0.42 um
Au_gam2 = val[8]*eV_um_scale
Au_sig2 = Au_f2*Au_plasma_frq**2/Au_frq2**2

Au_f3 = val[9]
Au_frq3 = val[10]*eV_um_scale      # 0.418 um
Au_gam3 = val[11]*eV_um_scale
Au_sig3 = Au_f3*Au_plasma_frq**2/Au_frq3**2

Au_f4 = val[12]
Au_frq4 = val[13]*eV_um_scale      # 0.288 um
Au_gam4 = val[14]*eV_um_scale
Au_sig4 = Au_f4*Au_plasma_frq**2/Au_frq4**2
Au_f5 = val[15]
Au_frq5 = val[16]*eV_um_scale      # 0.093 um
Au_gam5 = val[17]*eV_um_scale
Au_sig5 = Au_f5*Au_plasma_frq**2/Au_frq5**2


fx = val[18] + calcdrude(frequency=f, frequencyn=Au_frq0,
                         sigma=Au_sig0, gamma=Au_gam0)
fx = fx + calclorentizan(frequency=f, frequencyn=Au_frq1,
                         gamma=Au_gam1, sigma=Au_sig1)
fx = fx + calclorentizan(frequency=f, frequencyn=Au_frq2,
                         gamma=Au_gam2, sigma=Au_sig2)
fx = fx + calclorentizan(frequency=f, frequencyn=Au_frq3,
                         gamma=Au_gam3, sigma=Au_sig3)
fx = fx + calclorentizan(frequency=f, frequencyn=Au_frq4,
                         gamma=Au_gam4, sigma=Au_sig4)
fx = fx + calclorentizan(frequency=f, frequencyn=Au_frq5,
                         gamma=Au_gam5, sigma=Au_sig5)
# plt.figure(2)
# plt.subplot(121)
# plt.plot(1/f,np.real(fx),color = 'C1', label= 'changed real')
# plt.plot(1/f,np.imag(fx),color = 'C2' ,label= 'changed imaginery')
# plt.plot(1/f,np.real(au),color = 'C3', label= 'orjinal real')
# plt.plot(1/f,np.imag(au),color = 'C4' ,label= 'orjinal imaginery')
# plt.ylim(-14,6)
# plt.legend()
# plt.grid()
# plt.subplot(122)
plt.plot(1/f, np.real(fx), color='C1', label='changed real')
plt.plot(1/f, np.imag(fx), color='C2', label='changed imaginery')
plt.plot(1/f, np.real(mix1), color='C3', label='mix real')
plt.plot(1/f, np.imag(mix1), color='C4', label='mix imaginery')
plt.xlabel('Wavelengths  µm ')
plt.ylabel('Epsilon')
plt.legend()
plt.grid()
plt.show()
