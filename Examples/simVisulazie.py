import meep as mp
import numpy as np
import meep.visualization as vis
import matplotlib.pyplot as plt
cell = mp.Vector3(16,8,10)
geometry = [mp.Block(mp.Vector3(5,5,5),
                     center=mp.Vector3(),
                     material=mp.Medium(epsilon=12))]

sources = [mp.Source(mp.ContinuousSource(frequency=0.15),
                     component=mp.Ez,
                     center=mp.Vector3(-7,0))]

pml_layers = [mp.PML(1.0)]

resolution = 10

sim = mp.Simulation(cell_size=cell,
                    dimensions=3,
                    boundary_layers=pml_layers,
                    geometry=geometry,
                    sources=sources,
                    resolution=resolution)
sim.init_sim()
print(type(sim.get_epsilon()))
# plt.plot(sim.get_epsilon())
# plt.show()
#sim.run(until=200)
arr=sim.get_epsilon()
from numpy import save
save("test.npy",arr)