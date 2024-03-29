import numpy as np
from numpy.core.defchararray import array
from numpy.lib.npyio import save
import scipy.optimize as opt
import pandas as pd
from functions import calcdrude, calclorentizan, mixsolver
import matplotlib.pyplot as plt
from numpy import load
guesses = load("guess.npy")
# gold is 0
or0 = np.array([[0, 0, 0, 0], [0.2, 0.4, 0.6, 0.8], [0.8, 0.6, 0.4, 0.2]])
o9 = np.array([or0[::, 0], or0[::, 1], or0[::, 2], or0[::, 3]])

# gold is 0
or0 = np.array([[0.2, 0.4, 0.6, 0.8], [0, 0, 0, 0], [0.8, 0.6, 0.4, 0.2]])
o10 = np.array([or0[::, 0], or0[::, 1], or0[::, 2], or0[::, 3]])

# gold is 0
or0 = np.array([[0.2, 0.4, 0.6, 0.8], [0.8, 0.6, 0.4, 0.2], [0, 0, 0, 0]])
o11 = np.array([or0[::, 0], or0[::, 1], or0[::, 2], or0[::, 3]])

# only gold silver pdms

o12 = np.array([[0, 0, 1], [0, 1, 0], [1, 0, 0]])
# gold is 0.25 and others are changing
or0 = np.array([[0.25, 0.25, 0.25, 0.25], [
               0.15, 0.3, 0.45, 0.6], [0.6, 0.45, 0.3, 0.15]])
o0 = np.array([or0[::, 0], or0[::, 1], or0[::, 2], or0[::, 3]])
#silver is 0.25
or0 = np.array([[0.15, 0.3, 0.45, 0.6], [0.25, 0.25,
                                         0.25, 0.25], [0.6, 0.45, 0.3, 0.15]])
o1 = np.array([or0[::, 0], or0[::, 1], or0[::, 2], or0[::, 3]])
# pdms is 0.25
or0 = np.array([[0.15, 0.3, 0.45, 0.6], [0.6, 0.45,
                                         0.3, 0.15], [0.25, 0.25, 0.25, 0.25]])
o2 = np.array([or0[::, 0], or0[::, 1], or0[::, 2], or0[::, 3]])

# gold is 0.5
or0 = np.array(
    [[0.5, 0.5, 0.5, 0.5], [0.1, 0.2, 0.3, 0.4], [0.4, 0.3, 0.2, 0.1]])
o3 = np.array([or0[::, 0], or0[::, 1], or0[::, 2], or0[::, 3]])
# silver is 0.5
or0 = np.array(
    [[0.1, 0.2, 0.3, 0.4], [0.5, 0.5, 0.5, 0.5], [0.4, 0.3, 0.2, 0.1]])
o4 = np.array([or0[::, 0], or0[::, 1], or0[::, 2], or0[::, 3]])
# pdms 0.5
or0 = np.array(
    [[0.1, 0.2, 0.3, 0.4], [0.4, 0.3, 0.2, 0.1], [0.5, 0.5, 0.5, 0.5]])
o5 = np.array([or0[::, 0], or0[::, 1], or0[::, 2], or0[::, 3]])

#gold is 0.75
or0 = np.array([[0.75, 0.75, 0.75, 0.75], [
               0.05, 0.1, 0.15, 0.2], [0.2, 0.15, 0.1, 0.05]])
o6 = np.array([or0[::, 0], or0[::, 1], or0[::, 2], or0[::, 3]])
# silver is 0.75
or0 = np.array([[0.05, 0.1, 0.15, 0.2], [0.75, 0.75,
                                         0.75, 0.75], [0.2, 0.15, 0.1, 0.05]])
o7 = np.array([or0[::, 0], or0[::, 1], or0[::, 2], or0[::, 3]])
# pdms is 0.75
or0 = np.array([[0.05, 0.1, 0.15, 0.2], [0.2, 0.15,
                                         0.1, 0.05], [0.75, 0.75, 0.75, 0.75]])
o8 = np.array([or0[::, 0], or0[::, 1], or0[::, 2], or0[::, 3]])
o = [o0, o1, o2, o3, o4, o5, o6, o7, o8, o9, o10, o11]

o = np.reshape(o, (np.int(np.size(o)/3), 3))
o = np.append(o, o12)
o = np.reshape(o, (np.int(np.size(o)/3), 3))

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

out = guesses
counter = 0
maxerror = []
for j in o:
    if np.count_nonzero(j == 0) == 0:
        mix1 = mixsolver([j[0], j[1], j[2]], auorj, agorj, polimer)
    elif np.count_nonzero(j == 0) == 1:
        index = np.where(j == 0)
        if (index == np.array([0])).all():
            mix1 = mixsolver([j[1], j[2]], agorj, polimer)

        elif (index == np.array([1])).all():
            mix1 = mixsolver([j[0], j[2]], auorj, polimer)
        else:
            mix1 = mixsolver([j[0], j[1]], auorj, agorj)
    else:
        index = np.where(j == 1)
        if (index == np.array([0])).all():
            mix1 = np.array(auorj)

        elif (index == np.array([1])).all():
            mix1 = np.array(agorj)

        else:
            mix1 = polimer

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

    bnds = opt.Bounds([-np.inf, 1e-10, 1e-10, 1e-10, -np.inf, 1e-10, 1e-10, 1e-10, 1e-10, 1e-10, 1e-10, 1e-10, 1e-10, 1e-10, 1e-10, 1e-10, 1e-10, 1e-10, 1],
                      [np.inf, np.inf, np.inf, np.inf, 30, np.inf, np.inf, 30, np.inf,
                       np.inf, 30, np.inf, np.inf, 30, np.inf, np.inf, 30, np.inf, 10], True)

    i = 1
    guess = out[counter]
    while i != 0:
        a = opt.minimize(fun1, guess, method="L-BFGS-B", bounds=bnds,
                         options={'maxiter': 1e6}, tol=0)
        # print(a)
        print(a.fun)

        print(i)
        guess = a.x
        i = i-1
    maxerror.append(a.fun)
    val = a.x
    out[counter] = val
    counter += 1
    # Au_plasma_frq = val[0]*eV_um_scale

    # Au_f0 = val[1]
    # Au_frq0 = 1e-10
    # Au_gam0 = val[2]*eV_um_scale
    # Au_sig0 = Au_f0*Au_plasma_frq**2/Au_frq0**2

    # Au_f1 = val[3]
    # Au_frq1 = val[4]    # 0.42 um
    # Au_gam1 = val[5]*eV_um_scale
    # Au_sig1 = Au_f1*Au_plasma_frq**2/Au_frq1**2

    # Au_f2 = val[6]
    # Au_frq2 = val[7]   # 0.42 um
    # Au_gam2 = val[8]*eV_um_scale
    # Au_sig2 = Au_f2*Au_plasma_frq**2/Au_frq2**2

    # Au_f3 = val[9]
    # Au_frq3 = val[10]*eV_um_scale      # 0.418 um
    # Au_gam3 = val[11]*eV_um_scale
    # Au_sig3 = Au_f3*Au_plasma_frq**2/Au_frq3**2

    # Au_f4 = val[12]
    # Au_frq4 = val[13]*eV_um_scale      # 0.288 um
    # Au_gam4 = val[14]*eV_um_scale
    # Au_sig4 = Au_f4*Au_plasma_frq**2/Au_frq4**2
    # Au_f5 = val[15]
    # Au_frq5 = val[16]*eV_um_scale      # 0.093 um
    # Au_gam5 = val[17]*eV_um_scale
    # Au_sig5 = Au_f5*Au_plasma_frq**2/Au_frq5**2

    # fx = val[18] + calcdrude(frequency=f, frequencyn=Au_frq0,
    #                          sigma=Au_sig0, gamma=Au_gam0)
    # fx = fx + calclorentizan(frequency=f, frequencyn=Au_frq1,
    #                          gamma=Au_gam1, sigma=Au_sig1)
    # fx = fx + calclorentizan(frequency=f, frequencyn=Au_frq2,
    #                          gamma=Au_gam2, sigma=Au_sig2)
    # fx = fx + calclorentizan(frequency=f, frequencyn=Au_frq3,
    #                          gamma=Au_gam3, sigma=Au_sig3)
    # fx = fx + calclorentizan(frequency=f, frequencyn=Au_frq4,
    #                          gamma=Au_gam4, sigma=Au_sig4)
    # fx = fx + calclorentizan(frequency=f, frequencyn=Au_frq5,
    #                          gamma=Au_gam5, sigma=Au_sig5)
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

    # plt.plot(1/f, np.real(fx), color='C1', label='changed real')
    # plt.plot(1/f, np.imag(fx), color='C2', label='changed imaginery')
    # plt.plot(1/f, np.real(mix1), color='C3', label='mix real')
    # plt.plot(1/f, np.imag(mix1), color='C4', label='mix imaginery')
    # plt.xlabel('Wavelengths  µm ')
    # plt.ylabel('Epsilon')
    # plt.legend()
    # plt.grid()
    # plt.show()
save("guess.npy", out)
print(maxerror)
