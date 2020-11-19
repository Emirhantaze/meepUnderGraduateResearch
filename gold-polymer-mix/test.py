from meep.materials import Au, Ag
from numpy.core.function_base import linspace
from functions import mixsolver
import numpy as np
import matplotlib.pyplot as plt

# a = [1+2j, 1+2j, 1+2j]
# print(np.imag(a))
f = linspace(0.3, 0.8, 500)
a1 = np.round(Au.epsilon(1/f)[:, 0, 0], 3)
a2 = np.round(Ag.epsilon(1/f)[:, 0, 0], 3)
mix1 = np.empty(len(f), dtype=np.cdouble)
mix2 = np.empty(len(f), dtype=np.cdouble)
roots = []

mix2 = mixsolver(0.5, a1, a2)
# plt.plot(f, np.real(mix1), color="C1", label="new real")
# plt.plot(f, np.imag(mix1), color="C2", label="new imag")
plt.plot(f, np.real(mix2), color="C3", label="old real")
plt.plot(f, np.imag(mix2), color="C4", label="old imag")
plt.plot(f, np.real(a1), color="C5", label="gold real")
plt.plot(f, np.imag(a1), color="C6", label="gold imag")
plt.plot(f, np.real(a2), color="C7", label="silver real")
plt.plot(f, np.imag(a2), color="C8", label="silver imag")


plt.xlabel('Wavelengths  µm ')
plt.ylabel('Epsilon')
plt.legend()
plt.grid()
plt.show()
