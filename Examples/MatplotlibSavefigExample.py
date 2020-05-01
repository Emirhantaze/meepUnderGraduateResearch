import matplotlib.pyplot as plt
import numpy as np

t = np.arange(0,1,.001)
f = np.sin(2*3.14*t)
plt.plot(t,f,color="C1",label="test")

plt.legend()
plt.savefig(fname="/home/emirhan/meepUnderGraduateResearch/pictures/test.svg",format="svg")