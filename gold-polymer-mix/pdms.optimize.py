import numpy as np
import pandas as pd 
import scipy.optimize as opt
import matplotlib.pyplot as plt

df = pd.read_csv (r'./gold-polymer-mix/pdms.csv')
polimer = df['n'].to_numpy()
w = df['Wavelength, µm'].to_numpy()


def fun(x):
    f = (x[0]*x[4]**((x[1]/w)+x[2]))+x[3] # pdms'in fonksiyonu
    lastr = np.corrcoef(polimer,f)[1][0]
    last = np.sum((polimer-f)**2)*200
    print(last-lastr)
    return last-lastr

x = [ 0.00555007,  0.5687775 , -0.40683289,  1.39844407,  4.66929214]

a = opt.minimize(fun, x ,options={'maxiter':1e4},tol=0)
print(a)
x = a.x
f = (x[0]*x[4]**((x[1]/w)+x[2])) + x[3]

plt.plot(w,f,color="C1",label="üretilmiş")
plt.plot(w,polimer,color="C3",label="orjınal")
plt.xlabel('Wavelengths  µm ')
plt.ylabel('n')
plt.legend()
plt.grid()
plt.show()