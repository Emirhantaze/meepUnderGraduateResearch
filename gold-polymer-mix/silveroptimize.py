import numpy as np
import pandas as pd
import scipy.optimize as opt
from meep.materials import Au, Ag
from functions import calcdrude, calclorentizan, mixsolver
import matplotlib.pyplot as plt


ORAN = 0.3


df = pd.read_csv(r'./gold-polymer-mix/SilverMcPeak2015.csv')
w = df['Wavelength, µm'].to_numpy()
n = df['n'].to_numpy()
k = df['k'].to_numpy()
auorj = (n + k*1j)**2
f = 1/w
um_scale = 1.0
# conversion factor for eV to 1/um [=1/hc]
eV_um_scale = um_scale/1.23984193
# first drude


def findvalue(w, wfull, f):
    i = 0
    while(wfull[i] < w):
        i += 1
    i += -1

    return f[i]+(np.diff(f)[i]*((w-wfull[i])/np.diff(wfull)[i]))


au = Ag.epsilon(f)[:, 0, 0]
auorj = au
polimer = np.empty(len(auorj), dtype=np.cdouble)
x = [0.00555007,  0.5687775, -0.40683289,  1.39844407,  4.66929214]
polimer = (x[0]*x[4]**((x[1]/w)+x[2])) + x[3]
polimer = polimer**2
mix1 = np.empty(len(auorj), dtype=np.cdouble)
for i in range(len(auorj)):
    mix1[i] = mixsolver(ORAN, auorj[i], polimer[i])
    # mix1[i] = auorj[i]


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
    print(x)
    return x
    # sortedreal = np.sum(np.sort(np.real(last)**2)[113:])
    # sortedimag = np.sum(np.sort(np.imag(last)**2)[113:])
    # return (sortedreal + sortedimag)/28


bnds = ((1e-10, None), (1e-10, None), (1e-10, None), (1e-10, None), (1e-10, None), (1e-10, None), (1e-10, None), (1e-10, None), (1e-10, None), (1e-10, None), (1e-10, None), (1e-10, None), (1e-10, None), (1e-10, None),
        (1e-10, None), (1e-10, None), (1e-10, None), (1e-10, None))
bnds = opt.Bounds([-np.inf, -10, 1e-10, 1e-10, -np.inf, 1e-10, 1e-10, -np.inf, 1e-10, 1e-10, -np.inf, 1e-10, 1e-10, -np.inf, 1e-10, 1e-10, -np.inf, 1e-10, 100e-2],
                  [np.inf, np.inf, np.inf, np.inf, np.inf, np.inf, np.inf, np.inf, np.inf,
                   np.inf, np.inf, np.inf, np.inf, np.inf, np.inf, np.inf, np.inf, np.inf, 10], True)
# bnds = opt.Bounds(1e-10,10000,True)
if(ORAN == 0.1):
    # for 0.1 portion

    guess = [1.55189904e+00, 1.00000000e-10, 1.34729722e+01, 6.21542243e+00,
             7.49556943e-01, 9.12132993e-01, 1.02040978e+00, 1.66064878e+00,
             9.43315934e-01, 2.47924148e-01, 2.78533391e+00, 3.53457635e-01,
             1.01588180e+00, 3.10462249e+00, 5.42842755e-01, 6.11837135e+00,
             3.91524252e+00, 1.00000000e-10, 1.00000000e+00]
elif(ORAN == 0.2):
    # for 0.2 portion

    guess = [1.55189904e+00, 1.00000000e-10, 1.34729722e+01, 6.21542243e+00,
             7.49556943e-01, 9.12132993e-01, 1.02040978e+00, 1.66064878e+00,
             9.43315934e-01, 2.47924148e-01, 2.78533391e+00, 3.53457635e-01,
             1.01588180e+00, 3.10462249e+00, 5.42842755e-01, 6.11837135e+00,
             3.91524252e+00, 1.00000000e-10, 1.00000000e+00]

elif(ORAN == 0.3):

    # for 0.3 portion
    guess = [0.56430703, 30.48010254,  0.07630614, 12.74197104,  1.0672699,
             0.93341363,  1.81751608,  1.52663013, 24.17147764, 19.58574582,
             1.9763325,  1.84991224,  4.07992493,  6.20157491, 13.94179412,
             28.76012336,  2.93951127,  2.68427712,  3.01346811]

elif(ORAN == 0.4):

    # for 0.4 portion

    guess = [0.56430703, 30.48010254,  0.07630614, 12.74197104,  1.0672699,
             0.93341363,  1.81751608,  1.52663013, 24.17147764, 19.58574582,
             1.9763325,  1.84991224,  4.07992493,  6.20157491, 13.94179412,
             28.76012336,  2.93951127,  2.68427712,  2.01346811]

elif(ORAN == 0.5):

    # for 0.5 portion

    guess = [6.68761611e-01, 3.80581957e+01, 1.00000000e-10, 1.05203633e+01,
             1.24936000e+00, 1.39159225e+00, 5.66026051e-01, 1.48334942e+00,
             2.41998961e+01, 1.26936203e+01, 2.25734381e+00, 2.30006497e+00,
             1.47654147e+00, 6.68514003e+00, 1.41484679e+01, 1.99989692e+01,
             3.06873768e+00, 3.10850935e+00, 2.09876013e+00]


elif(ORAN == 0.6):
    # for 0.6 portion

    guess = [8.18795549e-01, 4.12272976e+01, 1.00000000e-10, 9.03581597e-01,
             1.56128786e+00, 4.88388054e-01, 1.00000000e-10, 1.47725760e+00,
             2.42017690e+01, 3.83040522e+00, 2.31285954e+00, 1.05376096e+00,
             2.31904116e-01, 6.74215377e+00, 1.41862486e+01, 1.36473964e+01,
             3.15511091e+00, 2.21384531e+00, 2.29393935e+00]

elif(ORAN == 0.7):

    # for 0.7 portion

    guess = [9.62532338e-01, 4.22854258e+01, 9.12635787e-02, 3.64773800e-01,
             2.06707965e+00, 2.97372610e-01, 1.00000000e-10, 1.45435988e+00,
             2.41535461e+01, 1.18238939e+00, 2.84568945e+00, 5.29277362e-01,
             1.00000000e-10, 6.63112676e+00, 1.42162722e+01, 3.08940805e+00,
             3.37432195e+00, 6.81569617e-01, 2.46428643e+00]

elif(ORAN == 0.8):

    # for 0.8 portion

    guess = [4.43911224e+00, 2.44143359e+00, 5.57601993e-02, 7.55156769e-02,
             3.01596500e+00, 3.54279410e-01, 9.52180009e-01, 1.45903234e+00,
             2.41097092e+01, 2.63291812e+00, 6.89149420e+00, 1.00000000e-10,
             1.00000000e-10, 6.57135801e+00, 1.42196951e+01, 1.85281044e+00,
             2.12289394e+01, 6.93541687e+00, 1.00687934e+00]

elif(ORAN == 0.9):

    # for 0.9 portion

    guess = [4.71462610e+00, 2.64554501e+00, 5.76958262e-02, 3.22553897e-01,
             4.06336132e+00, 2.98261814e-01, 9.95191036e-01, 2.49680804e+00,
             2.41278000e+01, 9.09495002e-01, 8.13515082e+00, 8.46038802e-02,
             1.00000000e-10, 6.56820838e+00, 1.42216324e+01, 2.32442591e+00,
             2.10389762e+01, 7.07658803e+00, 1.59376956e+00]

""" original values of Ag
        guess = [9.01, 0.845,  0.048,  0.065, 3.886, 0.124,
    0.816,   4.481, 0.452,
    0.011, 8.185,  0.065, 0.840,
    9.083,  0.916,  5.646, 20.29, 2.419, 2.37087344e+00]
"""

a = opt.minimize(fun1, guess, method="L-BFGS-B", bounds=bnds,
                 options={'maxiter': 1e6}, tol=0)
print(a)
print(a.fun)
val = [6.02770302, 0.52555576, 0.559028, 2.22523591, 4.49832775,
       6.43146069, 0.0226519, 1.53130738, 0.63986773]
val = a.x
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

# plt.plot(f[1:len(f)],np.diff(np.imag(mix1)))

# plt.plot(f[2:len(f)],np.diff(np.diff(np.imag(mix1)))*5.1)
# plt.grid()
# plt.show()
