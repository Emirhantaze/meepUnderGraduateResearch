import numpy as np
import pandas as pd
import scipy.optimize as opt
from meep.materials import Au
from functions import calcdrude, calclorentizan, mixsolver
import matplotlib.pyplot as plt


ORAN = 0.9


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


# au = Au.epsilon(f)[:,0,0]
polimer = np.empty(len(auorj), dtype=np.cdouble)
x = [0.00555007,  0.5687775, -0.40683289,  1.39844407,  4.66929214]
polimer = (x[0]*x[4]**((x[1]/w)+x[2])) + x[3]
polimer = polimer**2
mix1 = np.empty(len(auorj), dtype=np.cdouble)
for i in range(len(auorj)):
    temp = np.roots(mixsolver(ORAN, auorj[i], polimer[i]))
    mix1[i] = temp[0]


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
bnds = opt.Bounds([-np.inf, -10, 1e-10, 1e-10, -np.inf, 1e-10, 1e-10, -np.inf, 1e-10, 1e-10, -np.inf, 1e-10, 1e-10, -np.inf, 1e-10, 1e-10, -np.inf, 1e-10, 44e-2],
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
    guess = [4.80356805e+00, -2.36949831e+00,  7.59186088e+00,  3.49093673e+01,
             1.69100619e+01,  4.49108524e+02, -4.01199801e-01,  1.83324169e+00,
             1.08705144e+00, -1.39827430e+00,  2.90556517e+00,  1.37106608e+00,
             -1.47240133e+01,  4.18449530e+00,  8.54448177e+00,  6.89631913e+00,
             2.89046067e+00,  2.60720843e+00,  6.25559066e-01]

elif(ORAN == 0.4):

    # for 0.4 portion

    guess = [1.34838676e+00, 1.00000000e-10, 1.34647873e+01, 8.97296436e+00,
             6.32379608e-01, 7.43462500e-01, 1.00000000e-10, 1.00000000e-10,
             1.57588335e+00, 1.59673438e+00, 2.00000369e+00, 9.48842434e-01,
             6.72023538e-01, 2.89049334e+00, 5.06863406e-01, 3.78504277e+00,
             3.51143233e+00, 6.41451882e-01, 2.41680535e+00]

elif(ORAN == 0.5):

    # for 0.5 portion

    guess = [1.59494391e+00, 1.00000000e-10, 1.35059776e+01, 9.04275486e+00,
             2.03823256e-03, 5.57132001e-01, 5.11096419e+00, 3.07038611e+00,
             2.69917661e-01, 1.21603262e+00, 2.03617915e+00, 1.05613396e+00,
             2.53356956e-01, 2.75265033e+00, 3.47707931e-01, 1.10361139e+00,
             3.06365318e+00, 5.84536890e-01, 1.69056771e+00]


elif(ORAN == 0.6):
    # for 0.6 portion

    guess = [1.85363891e+00, 1.00000000e-10, 1.35059494e+01, 9.08226291e+00,
             3.88960804e-05, 1.00000000e-10, 2.61699241e+00, 2.99609943e+00,
             1.00000000e-10, 7.51361132e-01, 2.05864823e+00, 7.71673604e-01,
             1.39971789e-01, 2.72306612e+00, 3.56756627e-01, 3.09821906e+00,
             3.13065592e+00, 1.12911764e+00, 2.14526970e+00]

elif(ORAN == 0.7):

    # for 0.7 portion

    guess = [2.30198919e+00, 1.00000000e-10, 1.35055163e+01, 9.44034985e+00,
             1.15389461e-07, 1.00000000e-10, 1.00000000e-10, 2.11120653e+00,
             1.48482852e+00, 4.55102547e-02, 2.28683418e+00, 2.30763563e-01,
             8.69164922e-01, 2.77465072e+00, 6.98504333e-01, 1.75176559e+00,
             3.33262868e+00, 7.39833429e-01, 4.44926251e+00]

elif(ORAN == 0.8):

    # for 0.8 portion

    guess = [2.56585904e+00, 5.41312887e-01, 1.34722815e+01, 9.31369499e+00,
             8.24073644e-07, 2.36648954e-04, 1.00000000e-10, 2.02697068e+00,
             1.49947299e+00, 1.68415862e-01, 2.65663214e+00, 3.36348966e-01,
             5.68494883e-01, 2.91251561e+00, 5.77904604e-01, 2.28981861e+00,
             3.49458098e+00, 8.28291250e-01, 4.08091959e+00]

elif(ORAN == 0.9):

    # for 0.9 portion

    guess = [9.01, 0.845,  0.048,  0.065, 3.886, 0.124,
             0.816,   4.481, 0.452,
             0.011, 8.185,  0.065, 0.840,
             9.083,  0.916,  5.646, 20.29, 2.419, 2.2]

""" original values of Ag
        guess = [9.01, 0.845,  0.048,  0.065, 3.886, 0.124,
    0.816,   4.481, 0.452,
    0.011, 8.185,  0.065, 0.840,
    9.083,  0.916,  5.646, 20.29, 2.419, 2.37087344e+00]
"""

a = opt.minimize(fun1, guess, method="Powell", bounds=bnds,
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
