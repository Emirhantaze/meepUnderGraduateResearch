import numpy as np
import scipy.optimize as opt

#Some variables
cost = np.array([1.800, 0.433, 0.180])
p = np.array([0.480, 0.080, 0.020])
e = np.array([0.744, 0.800, 0.142])

#Our function
fun = lambda x: np.sum(x*cost)

#Our conditions
# cond = ({'type': 'eq', 'fun': lambda x: np.sum(x) - 100},
#         {'type': 'ineq', 'fun': lambda x: np.sum(p*x) - 24},
#         {'type': 'ineq', 'fun': lambda x: np.sum(e*x) - 76},
#         {'type': 'ineq', 'fun': lambda x: -1*x[2] + 2})


bnds = ((0,100),(0,100),(0,100))
guess = [20,30,50]
a = opt.minimize(fun, guess, method='SLSQP', bounds=bnds)
print(a)
