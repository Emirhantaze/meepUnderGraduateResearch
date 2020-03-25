# -*- coding: utf-8 -*-

# From the Meep tutorial: plotting permittivity and fields of a straight waveguide
from __future__ import division

import meep as mp

cell = mp.Vector3(16,8,0)
wvl_min = 0.350
wvl_max = 0.750
frq_min = 1/wvl_max
frq_max = 1/wvl_min
frq_cen = 0.5*(frq_min+frq_max)
dfrq = frq_max-frq_min
nfrq = 100
geometry = []

sources = [mp.Source(mp.GaussianSource(frq_cen,fwidth=dfrq),
                     component=mp.Ez,
                     size=mp.Vector3(0,8),
                     center=mp.Vector3(-7,0))]

pml_layers = [mp.PML(1.0)]

resolution = 10

sim = mp.Simulation(cell_size=cell,
                    boundary_layers=pml_layers,
                    geometry=geometry,
                    sources=sources,
                    resolution=resolution)

sim.run(until=5)

import numpy as np
import matplotlib.pyplot as plt

eps_data = sim.get_array(center=mp.Vector3(), size=cell, component=mp.Dielectric)
plt.figure()
plt.imshow(eps_data.transpose(), interpolation='spline36', cmap='binary')
plt.axis('off')
plt.show()

ez_data = sim.get_array(center=mp.Vector3(), size=cell, component=mp.Ez)
plt.figure()
plt.imshow(eps_data.transpose(), interpolation='spline36', cmap='binary')
plt.imshow(ez_data.transpose(), interpolation='spline36', cmap='RdBu', alpha=0.9)
plt.axis('off')
plt.show()
