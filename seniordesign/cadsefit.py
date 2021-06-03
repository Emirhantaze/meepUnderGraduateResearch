import matplotlib.pyplot as plt
import scipy.optimize as opt
import pandas as pd
import numpy as np
from functions import calcdrude, calclorentizan, mixsolver
df = pd.read_csv("./seniordesign/cadmiumse.csv")
polimer = df['n'].to_numpy()
w = df['Wavelength. µm'].to_numpy()
n = df['n'].to_numpy()
k = df['k'].to_numpy()
auorj = (n + k*1j)**2
f = 1/w


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

    fx = x[9] + calcdrude(frequency=f, frequencyn=Au_frq0,
                          sigma=Au_sig0, gamma=Au_gam0)
    fx = fx + calclorentizan(frequency=f, frequencyn=Au_frq1,
                             gamma=Au_gam1, sigma=Au_sig1)
    fx = fx + calclorentizan(frequency=f, frequencyn=Au_frq2,
                             gamma=Au_gam2, sigma=Au_sig2)

    last = auorj-fx  # fx burada üreittiğimiz değerşler mix1 ise ulaşmaya çalıştığımız değerler

    return np.sum(abs(last))


    # sortedreal = np.sum(np.sort(np.real(last)**2)[113:])
    # sortedimag = np.sum(np.sort(np.imag(last)**2)[113:])
    # return (sortedreal + sortedimag)/28
guess = np.ones(10)
bnds = opt.Bounds([-np.inf, 1e-10, 1e-10, 1e-10, -np.inf, 1e-10, 1e-10, 1e-10, 1e-10, 1],
                  [np.inf, np.inf, np.inf, np.inf, 30, np.inf, np.inf, 30,  np.inf, 10], True)


a = opt.minimize(fun1, guess, bounds=bnds,
                 options={'maxiter': 1e6}, tol=0)
print(a)
x = a.x
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

fx = x[9] + calcdrude(frequency=f, frequencyn=Au_frq0,
                      sigma=Au_sig0, gamma=Au_gam0)
fx = fx + calclorentizan(frequency=f, frequencyn=Au_frq1,
                         gamma=Au_gam1, sigma=Au_sig1)
fx = fx + calclorentizan(frequency=f, frequencyn=Au_frq2,
                         gamma=Au_gam2, sigma=Au_sig2)


plt.plot(w, fx.real, label="fx real")
plt.plot(w, fx.imag, label="fx imag")
plt.plot(w, auorj.real, label="cdse real")
plt.plot(w, auorj.imag, label="cdse imag")
plt.legend()
plt.show()
