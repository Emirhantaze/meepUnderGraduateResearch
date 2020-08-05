import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime

Trey1 = np.loadtxt("TREy_1.txt")**2
TREy2 = np.loadtxt("TREy_2.txt")**2
TREy3 = np.loadtxt("TREy_3.txt")**2
TREy4 = np.loadtxt("TREy_4.txt")**2
TREy5 = np.loadtxt("TREy_5.txt")**2

Trez1 = np.loadtxt("TREz_1.txt")**2
TREz2 = np.loadtxt("TREz_2.txt")**2
TREz3 = np.loadtxt("TREz_3.txt")**2
TREz4 = np.loadtxt("TREz_4.txt")**2
TREz5 = np.loadtxt("TREz_5.txt")**2

Pr1 = Trey1/Trez1
Pr2 = TREy2/TREz2
Pr3 = TREy3/TREz3
Pr4 = TREy4/TREz4
Pr5 = TREy5/TREz5

w  = np.linspace(700,400,100)

plt.plot(w,Pr1,color="C1",label="PR1")
plt.plot(w,Pr2,color="C2",label="PR2")
plt.plot(w,Pr3,color="C3",label="PR3")
plt.plot(w,Pr4,color="C4",label="PR4")
plt.plot(w,Pr5,color="C5",label="PR5")
plt.title("Polarization ratio |Ey|^2/|Ez|^2 ")
plt.xlabel("Wavelengths")
plt.ylabel("Transmission")
plt.legend()
time = datetime.now().strftime("%d-%m-%Y_%I-%M-%S_%p")
name = __file__.split("/")
name=name[len(name)-1]
plt.savefig(fname=f"/home/emirhantaze/github/meepUnderGraduateResearch/pictures/{name}_{time}.svg",format="svg")

plt.show()