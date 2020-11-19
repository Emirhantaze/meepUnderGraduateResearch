from meep.materials import Ag, Au
import numpy as np
import scipy.optimize as opt
import matplotlib.pyplot as plt
from functions import mixsolver


def main(e1, e2, f):
    def const1(x):
        return e1+2*x[0]

    def const2(x):
        return e2+2*x[0]

    constraints = ({"type": "ineq", "fun": const1},
                   {"type": "ineq", "fun": const2})

    def minimize(x):
        e = x[0] + x[1] * 1j
        fun = (f*(e1-e)/(e1+2*e))+((1-f)*(e2-e)/(e2+2*e))
        print(fun)
        return np.abs(np.real(fun))+np.abs(np.imag(fun))

    guess = [-1.752932249456268, 2.54698340455265]

    a = opt.minimize(minimize, guess, method="cobyla",
                     options={'maxiter': 1e6}, tol=1e-15, constraints=constraints)
    print(a)
    print(a.fun)
    print(minimize(guess))
    return a.x[0] + a.x[1]*1j


wavelength = 0.4
f = 1/wavelength
print(f"{main(Au.epsilon(f)[0,0],Ag.epsilon(f)[0,0],0.5)} result of numeric")
print(
    f"{mixsolver(0.5,Au.epsilon(f)[0,0],Ag.epsilon(f)[0,0])}, result of equation root1")
