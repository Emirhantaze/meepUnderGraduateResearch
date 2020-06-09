import numpy as np
import pandas as pd 
import scipy.optimize as opt
from meep.materials import Au
from functions import calcdrude, calclorentizan, mixsolver
import matplotlib.pyplot as plt
from time import time
df = pd.read_csv (r'./gold-polymer-mix/RefractiveIndexINFO.csv')
polimer = df['n'].to_numpy()**2
t = time()
f =  np.linspace(0.35,0.7,101)
f = 1 / f 
um_scale = 1.0
# conversion factor for eV to 1/um [=1/hc]
eV_um_scale = um_scale/1.23984193
# first drude



au = Au.epsilon(f)[:,0,0]
mix1 = np.empty(101,dtype=np.cdouble)
for i in range(101):
    temp = np.roots(mixsolver(0.5,au[i],polimer[i]))
    mix1[i] = temp[0]


def fun1(x):

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




    fx =  1 + calcdrude(frequency= f,frequencyn=Au_frq0,sigma=Au_sig0,gamma=Au_gam0 )
    fx = fx + calclorentizan(frequency=f,frequencyn=Au_frq1,gamma=Au_gam1,sigma=Au_sig1)
    fx = fx + calclorentizan(frequency=f,frequencyn=Au_frq2,gamma=Au_gam2,sigma=Au_sig2)
  
    last = mix1-fx
    lasti = np.corrcoef(np.real(mix1),np.real(fx))[1][0]
    lastr = np.corrcoef(np.imag(mix1),np.imag(fx))[1][0]
    print(np.sum((np.real(last)**2)+(np.imag(last)**2))+2 -1*(lasti+lastr) )
    
    return np.abs(np.sum((np.real(last)**2)+(np.imag(last)**2))+2-lasti-lastr) 


bnds = ((1e-10,10),(1e-10,10),(1e-10,10),(1e-10,10),(1e-10,10),
    (1e-10,10),(1e-10,10),(1e-10,10),(1e-10,10))
guess = [6.02770301, 0.52555561, 0.55902795, 2.22523594, 4.49832787,
       6.43146064, 0.02265125, 1.53130677, 0.63986759]
a = opt.minimize(fun1, guess, method='SLSQP')
print(a)
val = [6.02770302, 0.52555576, 0.559028  , 2.22523591, 4.49832775,
       6.43146069, 0.0226519 , 1.53130738, 0.63986773]
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



fx =  1 + calcdrude(frequency= f,frequencyn=Au_frq0,sigma=Au_sig0,gamma=Au_gam0 )
fx = fx + calclorentizan(frequency=f,frequencyn=Au_frq1,gamma=Au_gam1,sigma=Au_sig1)
fx = fx + calclorentizan(frequency=f,frequencyn=Au_frq2,gamma=Au_gam2,sigma=Au_sig2)


plt.subplot(121)
plt.plot(1/f,np.real(fx),color = 'C1', label= 'changed real')
plt.plot(1/f,np.imag(fx),color = 'C2' ,label= 'changed imaginery')
plt.plot(1/f,np.real(au),color = 'C3', label= 'orjinal real')
plt.plot(1/f,np.imag(au),color = 'C4' ,label= 'orjinal imaginery')
plt.ylim(-14,6)
plt.legend()
plt.grid()
plt.subplot(122)
plt.plot(1/f,np.real(fx),color = 'C1', label= 'changed real')
plt.plot(1/f,np.imag(fx),color = 'C2' ,label= 'changed imaginery')
plt.plot(1/f,np.real(mix1),color = 'C3', label= 'mix real')
plt.plot(1/f,np.imag(mix1),color = 'C4' ,label= 'mix imaginery')
plt.ylim(-14,6)
plt.legend()
plt.grid()
plt.show()

# plt.plot(f[1:len(f)],np.diff(np.imag(mix1)))
 
# plt.plot(f[2:len(f)],np.diff(np.diff(np.imag(mix1)))*5.1)
# plt.grid()
# plt.show()
