import numpy as np
import pandas as pd 
import scipy.optimize as opt
from meep.materials import Au
from functions import calcdrude, calclorentizan, mixsolver
import matplotlib.pyplot as plt



df = pd.read_csv (r'./gold-polymer-mix/gold.csv')
w = df['Wavelength, µm'].to_numpy()
n = df['n'].to_numpy()
k = df['k'].to_numpy()
auorj = (n + k*1j)**2
f = 1/w
um_scale = 1.0
# conversion factor for eV to 1/um [=1/hc]
eV_um_scale = um_scale/1.23984193
# first drude
print(len(auorj))
def findvalue(w,wfull,f):
    i = 0 
    while(wfull[i]<w):
        i+=1
    i+=-1
   
    return f[i]+(np.diff(f)[i]*((w-wfull[i])/np.diff(wfull)[i]))

# au = Au.epsilon(f)[:,0,0]
polimer = np.empty(31,dtype=np.cdouble)
x = [ 0.00555007,  0.5687775 , -0.40683289,  1.39844407,  4.66929214]
polimer = (x[0]*x[4]**((x[1]/w)+x[2])) + x[3]
polimer = polimer**2
mix1 = np.empty(31,dtype=np.cdouble)
for i in range(31):
    temp = np.roots(mixsolver(.5,auorj[i],polimer[i]))
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
    fx =  x[18] + calcdrude(frequency= f,frequencyn=Au_frq0,sigma=Au_sig0,gamma=Au_gam0 )
    fx = fx + calclorentizan(frequency=f,frequencyn=Au_frq1,gamma=Au_gam1,sigma=Au_sig1)
    fx = fx + calclorentizan(frequency=f,frequencyn=Au_frq2,gamma=Au_gam2,sigma=Au_sig2)
    fx = fx + calclorentizan(frequency=f,frequencyn=Au_frq3,gamma=Au_gam3,sigma=Au_sig3)
    fx = fx + calclorentizan(frequency=f,frequencyn=Au_frq4,gamma=Au_gam4,sigma=Au_sig4)
    fx = fx + calclorentizan(frequency=f,frequencyn=Au_frq5,gamma=Au_gam5,sigma=Au_sig5)
  
    last = mix1-fx # fx burada üreittiğimiz değerşler mix1 ise ulaşmaya çalıştığımız değerler  
    # lasti = np.corrcoef(np.real(mix1),np.real(fx))[1][0]
    # lastr = np.corrcoef(np.imag(mix1),np.imag(fx))[1][0]
    # # https://en.wikipedia.org/wiki/Reduced_chi-squared_statistic
    # print ((np.sum((np.real(last)**2)+(np.imag(last)**2))+40-(20*lasti)-(20*lastr)) )
    x = ((np.sum(np.real(last)**2)/(0.001)) + (np.sum(np.imag(last)**2)/0.001))/(len(mix1)-1)
    # x burada fitting için kullandığımız ve azaltmaya çalıştığımız parametre    
    # print(x)
    # return (np.sum((np.real(last)**2)+(np.imag(last)**2))+40-(20*lasti)-(20*lastr))     
    assert x != np.nan, f'{x} is problematic'
    print(x)
    return x
    # sortedreal = np.sum(np.sort(np.real(last)**2)[113:])
    # sortedimag = np.sum(np.sort(np.imag(last)**2)[113:])
    # return (sortedreal + sortedimag)/28

bnds = ((1e-10,None),(1e-10,None),(1e-10,None),(1e-10,None),(1e-10,None),(1e-10,None)
    ,(1e-10,None),(1e-10,None),(1e-10,None),(1e-10,None),(1e-10,None),(1e-10,None),(1e-10,None),(1e-10,None),
    (1e-10,None),(1e-10,None),(1e-10,None),(1e-10,None))
bnds = opt.Bounds([1e-10,1e-10,1e-10,1e-10,1e-10,1e-10,1e-10,1e-10
                    ,1e-10,1e-10,1e-10,1e-10,1e-10,1e-10,1e-10,1e-10,1e-10,1e-10,1e-2],
                    [np.inf,np.inf,np.inf,np.inf,np.inf,np.inf,np.inf,np.inf,np.inf,
                    np.inf,np.inf,np.inf,np.inf,np.inf,np.inf,np.inf,np.inf,np.inf,2],True)
# bnds = opt.Bounds(1e-10,10000,True)   
# for 0.1 portion

# guess = [  6.92943996,  -1.98309853,   1.88815906,   9.01549148,
#        -33.66874604, -52.75904524,  -0.57709943,   1.63493821,
#          1.60002361,  -0.09840054,   2.87772041,   0.84582074,
#        -21.07213078,   6.36842167,  10.21818153,  38.79924463,
#          5.011252  ,  26.85696109 ]

# for 0.2 portion


# guess = [ 1.10984197e+01, -4.94146180e-01,  2.83234241e+00, -5.29482243e+01,
#         1.92246955e+01,  8.78070225e+00, -1.13728727e-01,  1.71909747e+00,
#         1.43221353e+00, -3.22878111e-02,  2.87537375e+00,  8.03446838e-01,
#        -5.59533379e+00,  5.16196522e+00,  5.79708495e+00,  2.39902720e+02,
#         2.50464798e+01,  2.01145313e+02]

# for 0.3 portion

# guess = [  4.50334297,  -2.36039523,   6.3147018 ,  35.33688502,
#         17.12595266, 447.7562717 ,  -0.49864533,   1.82311039,
#          1.11131965,  -1.38969897,   2.89362531,   1.37674726,
#        -14.3958354 ,   4.08436157,   8.77016004,   6.82182287,
#          2.8246126 ,   2.5755586       ]


# for 0.4 portion

# guess = [ 5.49645565e+00,  8.41155335e+00,  3.10831375e+00,  7.14304805e+00,
#         4.25491100e+00, -9.39237901e-01,  4.10046282e-01,  1.80530291e+00,
#         1.43417669e+00,  5.85596162e-02,  2.79232098e+00,  5.67627101e-01,
#         1.93434554e+00,  3.50282425e+00,  1.58195403e+00,  1.46116652e+02,
#         2.94579111e+00, -7.09372681e+01]

# for 0.5 portion
 
# guess = [ 6.72073787,  1.98706561, 12.37325883,  0.24236221, -0.44074002,
#        -0.20397064, -0.9460953 ,  2.16779386,  0.77247122,  3.80910191,
#         2.74773122,  0.73757202, -2.85234548,  2.76064519,  0.71839763,
#         1.08304032,  5.39057946,  0.68705033]
guess = [1.78289910e+00, 1.00000000e-10, 1.34729698e+01, 7.20369796e+00,
       1.42305295e-07, 5.73419200e-01, 9.53801633e-01, 1.64525252e+00,
       1.05086993e+00, 2.26832125e-01, 2.75847736e+00, 3.64135525e-01,
       9.40636909e-01, 3.07875936e+00, 5.89122140e-01, 4.27335633e+00,
       3.83059318e+00, 1.95411014e-01, 1.55790666e+00]


# for 0.6 portion
 
# guess = [  5.64428194,   1.25243118,  -0.30574465,   0.1042075 ,
#          2.38395438,   0.64152114,   0.41554229,   1.65701553,
#          1.5499717 ,   0.01825886,   2.6940419 ,   0.3269882 ,
#          9.7651524 ,   9.29551582, -13.88262442,   0.71636058,
#          3.68337649,   0.92962158        ]

# for 0.7 portion
 
# guess = [ 6.98702945e+00,  9.84128790e-01, -9.23116743e-03,  1.96876231e+00,
#         3.06956368e+00,  2.90461052e+00, -5.19779085e-03,  1.61938339e+00,
#         3.43779376e-01,  1.49121571e-02,  2.76102094e+00,  4.06203485e-01,
#         1.12304049e+01,  8.04845464e+00, -1.29516450e+00, -4.17429894e+01,
#         1.41113541e+01,  2.46201881e+01]

# for 0.8 portion
 
# guess = [ 1.05773309e+01,  5.82982440e-01,  1.90072181e-01,  2.44313570e+00,
#         5.08112382e+00,  6.25313108e+00, -2.71785482e-01,  2.07683725e+00,
#         6.28187483e-01,  2.67667562e-01,  2.58588531e+00,  6.16516033e-01,
#         8.19176355e-02,  3.00281820e+00,  1.21603696e+00, -6.61454715e+00,
#         5.08877835e+00,  1.01571912e+02]

# for 0.9 portion
 
# guess =  [10.40208132,  0.72858707,  0.16811264, -3.04805665,  1.5162227 ,
#        46.86576817, -0.22047695,  2.07322868,  0.58193263,  0.21902183,
#         2.58538766,  0.57364056,  0.11432802,  3.02047409,  1.23348503,
#         2.04971322,  5.79054288,  4.43902867      ]

a = opt.minimize(fun1, guess,method = "trust-constr",bounds=bnds,options={'maxiter':1e6}, tol = 0)
print(a)
print(a.fun)
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


fx =  val[18] + calcdrude(frequency= f,frequencyn=Au_frq0,sigma=Au_sig0,gamma=Au_gam0 )
fx = fx + calclorentizan(frequency=f,frequencyn=Au_frq1,gamma=Au_gam1,sigma=Au_sig1)
fx = fx + calclorentizan(frequency=f,frequencyn=Au_frq2,gamma=Au_gam2,sigma=Au_sig2)
fx = fx + calclorentizan(frequency=f,frequencyn=Au_frq3,gamma=Au_gam3,sigma=Au_sig3)
fx = fx + calclorentizan(frequency=f,frequencyn=Au_frq4,gamma=Au_gam4,sigma=Au_sig4)
fx = fx + calclorentizan(frequency=f,frequencyn=Au_frq5,gamma=Au_gam5,sigma=Au_sig5)
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
plt.plot(1/f,np.real(fx),color = 'C1', label= 'changed real')
plt.plot(1/f,np.imag(fx),color = 'C2' ,label= 'changed imaginery')
plt.plot(1/f,np.real(mix1),color = 'C3', label= 'mix real')
plt.plot(1/f,np.imag(mix1),color = 'C4' ,label= 'mix imaginery')
plt.xlabel('Wavelengths  µm ')
plt.ylabel('Epsilon')
plt.legend()
plt.grid()
plt.show()

# plt.plot(f[1:len(f)],np.diff(np.imag(mix1)))
 
# plt.plot(f[2:len(f)],np.diff(np.diff(np.imag(mix1)))*5.1)
# plt.grid()
# plt.show()
