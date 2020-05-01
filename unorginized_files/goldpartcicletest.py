import meep as mp
import numpy as np
import matplotlib.pyplot as plt
import math
from meep.materials import Au
r = 0.01
wvl = 0.01
cell_y = 2*(wvl+r)+0.01
cell_x = 2*(wvl+6*r)+0.3
pml = [mp.PML(wvl)]
cell_size  = mp.Vector3(cell_x,cell_y)
for i in range(80):
    sources = [mp.Source(mp.ContinuousSource(wavelength=(i+1)*0.01),component=mp.Ez,
                        center=mp.Vector3(-(cell_x/2)+wvl,0),size=mp.Vector3(0,cell_y-2*wvl,0))]
    geometry = [mp.Cylinder(material=Au,
                        height = 0,
                        center=mp.Vector3(),
                        radius=r)]
    resulation = 50
    sim = mp.Simulation(cell_size=cell_size,
                        boundary_layers=pml,
                        geometry=geometry,
                        sources=sources,
                        resolution=resulation)
    sim.run(until=10)
    eps_data = sim.get_array(center=mp.Vector3(), size=cell_size, component=mp.Dielectric)
    ez_data = sim.get_array(center=mp.Vector3(), size=cell_size, component=mp.Ez)
    plt.figure()
    plt.imshow(eps_data.transpose(), interpolation='spline36', cmap='binary')
    plt.imshow(ez_data.transpose(), interpolation='spline36', cmap='RdBu', alpha=0.9)
    plt.axis('off')
    plt.title(str((i+1)*0.04))
    plt.show()