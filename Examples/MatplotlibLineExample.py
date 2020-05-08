import matplotlib.pyplot as plt
import numpy as np

t = np.arange(0,1,.001)
f = np.sin(2*3.14*t)
plt.plot(t,f,color="C1",label="test")
f = np.sin(2*3.14*t) + 1
plt.plot(t,f,color="C2",label="test2")
plt.legend()
ax= plt.gca()
print(dir(ax))
plt.show()