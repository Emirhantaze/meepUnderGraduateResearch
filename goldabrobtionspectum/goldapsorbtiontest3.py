from __future__ import division
import meep as mp
import numpy as np
import matplotlib.pyplot as plt
import math
cell = mp.Vector3(4,2)
pml_layers=[mp.PML(0.5)]
r=0.1
sx=2
dpml=0.5
minwavelength=0.1
maxwavelength=1.1
minf=1/maxwavelength
maxf=1/minwavelength
fcen = (maxf+minf)/2  
df = maxf-minf
nfreq=250
resolution = 40
sources = [mp.Source(mp.GaussianSource(fcen,fwidth=df),
                     component=mp.Ez,   
                     center=mp.Vector3(-1.5,0,0),
                     size=mp.Vector3(0,0.5,0))]
sim = mp.Simulation(cell_size=cell,
                    boundary_layers=pml_layers,
                    sources=sources,
                    resolution=resolution)

lightside_fr = mp.FluxRegion(center=mp.Vector3(-1), 
                             size=mp.Vector3(0,1,0))
lightside = sim.add_flux(fcen, df ,nfreq,lightside_fr)
pt = mp.Vector3(0.5*sx-dpml-0.5,0)
sim.run(until_after_sources=mp.stop_when_fields_decayed(50,mp.Ez,pt,1e-3))
a=mp.get_fluxes(lightside)
a=a[(74+12):(249-75+12)]
f=np.linspace(800,400,100)
plt.plot(f,a)
plt.show()
#22:15 5saat 34 dk+