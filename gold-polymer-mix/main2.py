import numpy as np
from numpy.core.function_base import linspace
import pandas as pd
import scipy.optimize as opt
from meep.materials import Au
from functions import calcdrude, calclorentizan, mixsolver
import matplotlib.pyplot as plt


ORAN = 1


df = pd.read_csv(r'./gold-polymer-mix/goldMcPeak2015.csv')
w = df['Wavelength, µm'].to_numpy()
n = df['n'].to_numpy()
k = df['k'].to_numpy()
auorj = (n + k*1j)**2
f = 1/w
um_scale = 1.0
# conversion factor for eV to 1/um [=1/hc]
eV_um_scale = um_scale/1.23984193
# first drude


# w = linspace(0.38, 0.74, 50)
# f = 1/w
# auorj = Au.epsilon(f)[:, 0, 0]
polimer = np.empty(len(f), dtype=np.cdouble)
x = [0.00555007,  0.5687775, -0.40683289,  1.39844407,  4.66929214]
polimer = (x[0]*x[4]**((x[1]/w)+x[2])) + x[3]
polimer = polimer**2
if ORAN == 1:
    mix1 = auorj
else:
    mix1 = mixsolver(ORAN, auorj, polimer)


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
    # sortedreal = np.sum(np.sort(np.real(last)**2)[113:])
    # sortedimag = np.sum(np.sort(np.imag(last)**2)[113:])
    # return (sortedreal + sortedimag)/28


bnds = ((1e-10, None), (1e-10, None), (1e-10, None), (1e-10, None), (1e-10, None), (1e-10, None), (1e-10, None), (1e-10, None), (1e-10, None), (1e-10, None), (1e-10, None), (1e-10, None), (1e-10, None), (1e-10, None),
        (1e-10, None), (1e-10, None), (1e-10, None), (1e-10, None))
bnds = opt.Bounds([-np.inf, 1e-10, 1e-10, 1e-10, -np.inf, 1e-10, 1e-10, 1e-10, 1e-10, 1e-10, 1e-10, 1e-10, 1e-10, 1e-10, 1e-10, 1e-10, 1e-10, 1e-10, 1],
                  [np.inf, np.inf, np.inf, np.inf, 30, np.inf, np.inf, 30, np.inf,
                   np.inf, 30, np.inf, np.inf, 30, np.inf, np.inf, 30, np.inf, 10], True)
# bnds = opt.Bounds(1e-10,10000,True)
if(ORAN == 0.1):
    # for 0.1 portion

    guess = [9.77423308e-02, 1.00000000e-10, 8.97862938e-01, 1.00000000e-10,
             4.82050659e+01, 1.82514496e+02, 6.88382384e+01, 1.52658236e+00,
             3.68995631e-01, 1.53942725e+02, 2.18405623e+00, 5.75401154e-01,
             1.59761743e+02, 3.24374033e+00, 9.79274650e-01, 9.93593909e+00,
             1.66697557e+02, 2.76735037e+01, 2.49933040e+00]
elif(ORAN == 0.2):
    # for 0.2 portion

    guess = [1.30629985e-01, 2.26319869e+02, 1.00000000e-10, 2.17263249e-07,
             3.00000000e+01, 1.82514496e+02, 2.69231977e+02, 1.40201548e+00,
             8.60991162e-01, 5.63111849e+01, 2.17220096e+00, 5.41502956e-01,
             1.63446009e+02, 3.19364529e+00, 9.86096525e-01, 9.91367717e+00,
             2.99862012e+01, 2.76591242e+01, 3.30711256e+00]
elif(ORAN == 0.3):

    # for 0.3 portion
    guess = [2.23407973e-01,  5.14792781e+02,  2.20610555e+00,  1.00000000e-10,
             -1.19048744e+01,  4.52785777e+02,  1.00000000e-10,  3.84765045e-07,
             9.48874754e+01,  8.59917093e+00,  3.12400116e+00,  2.30285986e-01,
             1.00000000e-10,  6.19764794e+00,  4.16376252e+00,  1.00000000e-10,
             1.81777663e+01,  1.46038634e+00,  3.84012808e+00]

elif(ORAN == 0.4):

    # for 0.4 portion

    guess = [1.45281414e+00,  1.00000000e-10,  5.12707370e+00,  1.00000000e-10,
             -5.75533172e-02,  9.07139969e+00,  9.76852212e+00,  7.78836820e-01,
             1.75458771e+00,  1.00000000e-10,  2.95885460e+00,  1.98690451e+00,
             9.50460986e-01,  3.01177484e+00,  5.27344514e-01,  7.40361572e+00,
             3.82120021e+00,  1.00000000e-10,  1.00000000e+00]

elif(ORAN == 0.5):

    # for 0.5 portion

    guess = [2.02098616e+00,  1.00000000e-10,  1.00379993e+01,  5.65291831e+00,
             -2.01426547e-01,  7.40176922e-01,  6.32889402e+00,  3.31848610e+00,
             1.00000000e-10,  6.01909241e-01,  2.05745883e+00,  9.56468570e-01,
             9.46870604e-01,  3.11779840e+00,  6.31031437e-01,  2.04299862e-01,
             2.76875969e+00,  3.83478456e-01,  1.00000000e+00]


elif(ORAN == 0.6):
    # for 0.6 portion

    guess = [2.16259263e+00, 1.00000000e-10, 9.99864586e+00, 6.77999562e+00,
             2.91732544e-06, 1.00000000e-10, 3.97279462e+00, 3.11071965e+00,
             6.92561615e-01, 1.21718301e+00, 2.03876665e+00, 1.17459884e+00,
             7.57142007e-01, 3.01937987e+00, 6.54834836e-01, 1.50265412e-01,
             2.72111048e+00, 3.47122083e-01, 2.97199162e+00]

elif(ORAN == 0.7):

    # for 0.7 portion

    guess = [7.89023859e-01,  1.00000000e-10,  1.67467932e+01,  4.98362208e+01,
             -7.00431918e-01,  1.00000000e-10,  8.59155335e+00,  2.50397393e+00,
             5.75035873e-01,  1.70582701e+00,  2.19646729e+00,  3.76670026e-01,
             7.18336933e+00,  2.73208824e+00,  6.57561460e-01,  2.89820785e+01,
             3.69075060e+00,  1.00000000e-10,  1.00000000e+00]

elif(ORAN == 0.8):

    # for 0.8 portion

    guess = [2.20952072e+00, 1.00000000e-10, 3.08307514e+00, 1.30451977e+01,
             8.66834886e-07, 1.00000000e-10, 1.00000000e-10, 1.58390897e+00,
             2.45891641e-01, 1.00000000e-10, 4.55795528e-01, 5.61822309e+00,
             1.33127364e+00, 2.78073316e+00, 7.51456359e-01, 2.23177537e+00,
             3.33520907e+00, 7.08755770e-01, 5.84861626e+00]

elif(ORAN == 0.9):

    # for 0.9 portion

    guess = [3.99837366e-01,  7.64489707e+00,  2.40469605e+00,  4.64672954e+02,
             -1.17204935e-04,  8.70368299e-05,  4.00584260e+01,  2.37950237e+00,
             6.66585589e-01,  1.40037739e-02,  2.74904798e+01,  1.83602964e+01,
             1.11445924e+01,  2.66217030e+00,  3.96599205e-01,  9.80600767e+01,
             3.51300897e+00,  6.53023813e-01,  5.39260635e+00]
elif(ORAN == 1):

    # for 1 portion

    guess = [2.74596985e+00,  2.55454715e-01,  8.30476963e+00,  1.10151790e+01,
             -2.39854301e-01,  1.00000000e-10,  9.30170074e-02,  2.10186777e+00,
             2.44996696e-01,  4.24986161e+00,  3.73509890e+00,  1.00135561e+00,
             2.49007699e-01,  2.76360724e+00,  3.71637890e-01,  6.68914595e-01,
             3.00816822e+00,  5.91449138e-01,  4.46871264e+00]
i = 10
while i != 0:
    a = opt.minimize(fun1, guess, method="L-BFGS-B", bounds=bnds,
                     options={'maxiter': 1e6}, tol=0)
    print(a)
    print(a.fun)
    print(i)
    guess = a.x
    i = i-1
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
