from __future__ import division
import meep as mp
import numpy as np
import matplotlib.pyplot as plt
import math
from meep.materials import Au
cell = mp.Vector3(0.12,0.12)
pml_layers=[mp.PML(0.01)]

sx=0.12
#Au = mp.Medium(index=math.pow(6.9,(1/2)))
dpml=0.01
minwavelength=0.4
maxwavelength=0.8
minf=1/maxwavelength
maxf=1/minwavelength
fcen = (maxf+minf)/2
df = maxf-minf
nfreq=100
resolution = 100
sources = [mp.Source(mp.GaussianSource(fcen,fwidth=df,is_integrated=True),
                     component=mp.Ey,
                     center=mp.Vector3(-0.05,0,0),
                     size=mp.Vector3(0,0.12,0))]
                     
sim = mp.Simulation(cell_size=cell,
                    boundary_layers=pml_layers,
                    k_point=mp.Vector3(),
                    sources=sources,
                    default_material=mp.Medium(epsilon=1.78),
                    resolution=resolution)


#for i in (np.arange(1,3)):
#    r=i*0.01
r=0.02
sim = mp.Simulation(cell_size=cell,
                    boundary_layers=pml_layers,
                    sources=sources,
                    resolution=resolution)
left_fr = mp.FluxRegion(center=mp.Vector3(x=-r),
                             size=mp.Vector3(0,2*r,0))
left_monitor = sim.add_flux(fcen, df ,nfreq,left_fr)
    
right_fr = mp.FluxRegion(center=mp.Vector3(x=r),
                             size=mp.Vector3(0,2*r,0))
right_monitor = sim.add_flux(fcen, df ,nfreq,right_fr)
    
top_fr = mp.FluxRegion(center=mp.Vector3(y=r),
                             size=mp.Vector3(2*r,0,0))
top_monitor = sim.add_flux(fcen, df ,nfreq,top_fr)
    
bottom_fr = mp.FluxRegion(center=mp.Vector3(y=-r),
                             size=mp.Vector3(2*r,0,0))
bottom_monitor = sim.add_flux(fcen, df ,nfreq,bottom_fr)
    
pt = mp.Vector3(0.5*sx-dpml-0.01,0)
sim.run(until_after_sources=mp.stop_when_fields_decayed(50,mp.Ez,pt,1e-3))
    
left_flux_data = sim.get_flux_data(left_monitor)
right_flux_data = sim.get_flux_data(right_monitor)
top_flux_data = sim.get_flux_data(top_monitor)
bottom_flux_data = sim.get_flux_data(bottom_monitor)
    
left_flux0 = mp.get_fluxes(left_monitor)
right_flux0 = mp.get_fluxes(right_monitor)
top_flux0 = mp.get_fluxes(top_monitor)
bottom_flux0 = mp.get_fluxes(bottom_monitor)
    
sim.reset_meep()
    
geometrys = [mp.Cylinder(material=Au,radius=r,center=mp.Vector3())]
sim = mp.Simulation(cell_size=cell,
                    geometry=geometrys,
                    boundary_layers=pml_layers,
                    sources=sources,
                    resolution=resolution)
    
left_monitor = sim.add_flux(fcen, df ,nfreq,left_fr)
right_monitor = sim.add_flux(fcen, df ,nfreq,right_fr)
top_monitor = sim.add_flux(fcen, df ,nfreq,top_fr)
bottom_monitor = sim.add_flux(fcen, df ,nfreq,bottom_fr)
    
sim.load_minus_flux_data(left_monitor,left_flux_data)
sim.load_minus_flux_data(right_monitor,right_flux_data)
sim.load_minus_flux_data(top_monitor,top_flux_data)
sim.load_minus_flux_data(bottom_monitor,bottom_flux_data)
    
pt = mp.Vector3(0.5*sx-dpml-0.01,0)
sim.run(until_after_sources=mp.stop_when_fields_decayed(50,mp.Ez,pt,1e-5))
    
    
left_flux=mp.get_fluxes(left_monitor)
right_flux=mp.get_fluxes(right_monitor)
top_flux=mp.get_fluxes(top_monitor)
bottom_flux=mp.get_fluxes(bottom_monitor)

scatt_flux=np.asarray(left_flux)-np.asarray(right_flux)+np.asarray(bottom_flux)-np.asarray(top_flux)
#scatt_flux=abs(np.asarray(left_flux))+abs(np.asarray(right_flux))+abs(np.asarray(bottom_flux))+abs(np.asarray(top_flux))
incident = abs(np.asarray(left_flux0))

scatt_ratio = np.divide(scatt_flux,incident)

freqs = mp.get_flux_freqs(left_monitor)
wavelengths = np.divide(1,freqs)
plt.figure()
plt.plot(wavelengths,scatt_ratio,'r',label='abs 20')

plt.legend(loc="upper right")
plt.show()
