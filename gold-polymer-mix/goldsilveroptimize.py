from meep.materials import Ag, Au
import numpy as np
import scipy.optimize as opt
from functions import calcdrude, calclorentizan, mixsolver
import matplotlib.pyplot as plt
um_scale = 1.0
# conversion factor for eV to 1/um [=1/hc]
eV_um_scale = um_scale/1.23984193
ORAN = 0.1
wavelengths = np.linspace(0.3, 0.7, 300)

f = 1/wavelengths

ag = Ag.epsilon(f)[:, 0, 0]
au = Au.epsilon(f)[:, 0, 0]
mix1 = np.empty(len(f), dtype=np.cdouble)

for i in range(len(f)):
    mix1[i] = mixsolver(ORAN, au[i], ag[i])


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


guess = [-1.05518558e+02, -9.89165257e+00,  3.32630530e+01,  6.22738772e-01,
         -2.92629862e-01,  2.11432254e+00,  8.33337260e-06,  1.68303743e+00,
         2.40085562e+01,  4.29704726e-01,  7.51748770e+00,  2.85821078e+00,
         2.96126696e+00,  5.07206294e+00,  1.31613113e+01,  7.80482816e-01,
         2.51750508e+01,  7.30018266e+00,  7.22231399e+00]

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
# plt.plot(1/f, np.imag(au), color='C5', label='au imaginery')
# plt.plot(1/f, np.real(au), color='C6', label='au real')
# plt.plot(1/f, np.imag(ag), color='C7', label='ag imaginery')
# plt.plot(1/f, np.imag(ag), color='C8', label='ag real')

plt.xlabel('Wavelengths  µm ')
plt.ylabel('Epsilon')
plt.legend()
plt.grid()
plt.show()

# plt.plot(f[1:len(f)],np.diff(np.imag(mix1)))

# plt.plot(f[2:len(f)],np.diff(np.diff(np.imag(mix1)))*5.1)
# plt.grid()
# plt.show()
