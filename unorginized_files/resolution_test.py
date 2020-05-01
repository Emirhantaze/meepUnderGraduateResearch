from __future__ import division
import meep as mp

cell = mp.Vector3(0.1,0.1,0)
block_thicknessy = 0.01
block_thicknessx = 0.01
geometry=[mp.Block(mp.Vector3(block_thicknessx,block_thicknessy),
                    center=mp.Vector3(),
                    material=mp.Medium(epsilon=12))]

sources = [mp.Source(mp.ContinuousSource(frequency=0.15),
                     component=mp.Ez,
                     center=mp.Vector3(0,0))]


resolution = 1000
pml_layers= [mp.PML(0.01)]
sim = mp.Simulation(cell_size=cell,
                    eps_averaging=False,
                    boundary_layers=pml_layers,
                    geometry=geometry,
                    sources=sources,
                    resolution=resolution)



import numpy as np
import matplotlib.pyplot as plt

sim.plot2D()
plt.show()