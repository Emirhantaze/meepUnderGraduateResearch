from __future__ import division
import meep as mp
import numpy as np
import matplotlib.pyplot as plt
import math
from meep.materials import Au

pml_layers=[mp.PML(0.01)]

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


innerside_without_flux = []
otherside_without_flux = []
innerside_with_flux = []
lightside_with_flux = []
otherside_with_flux = []
indecentflux = []

for i in (np.arange(1,5)):
    r=i*0.005
    sx=12*r+2*dpml
    cell = mp.Vector3(sx,sx)
    sources = [mp.Source(mp.GaussianSource(fcen,fwidth=df),
                     component=mp.Ey,   
                     center=mp.Vector3(-0.05*(sx-2*dpml),0,0),
                     size=mp.Vector3(0,sx,0))]
    sim = mp.Simulation(cell_size=cell,
                    boundary_layers=pml_layers,
                    sources=sources,
                    resolution=resolution)
    lightside_fr = mp.FluxRegion(center=mp.Vector3(-2*r), 
                             size=mp.Vector3(0,4*r,0))
    lightside = sim.add_flux(fcen, df ,nfreq,lightside_fr)
    otherside_fr = mp.FluxRegion(center=mp.Vector3(2*r), 
                             size=mp.Vector3(0,4*r,0))
    otherside = sim.add_flux(fcen, df ,nfreq,otherside_fr)
    innerside_fr = mp.FluxRegion(center=mp.Vector3(0,2*r), 
                             size=mp.Vector3(4*r,0,0),
                             )
    incedent_fr = mp.FluxRegion(center=mp.Vector3(0.5*sx-dpml-0.01),size= mp.Vector3(0,sx))
    incedent = sim.add_flux(fcen, df ,nfreq,incedent_fr)
    innerside = sim.add_flux(fcen, df ,nfreq,innerside_fr)
    pt = mp.Vector3(0.5*sx-dpml-0.01,0)
    sim.run(until_after_sources=mp.stop_when_fields_decayed(50,mp.Ez,pt,1e-3))
    lightside_without_flux_data = sim.get_flux_data(lightside)
    innerside_without_flux_data = sim.get_flux_data(innerside)
    otherside_without_flux_data= sim.get_flux_data(otherside)
    indecentflux = np.append(indecentflux,mp.get_fluxes(incedent))
    a=mp.get_fluxes(otherside)
    #a=a[(74+12):(249-75+12)]
    otherside_without_flux = np.append(otherside_without_flux,a)
    innerside_without_flux = np.append(innerside_without_flux,mp.get_fluxes(innerside))
    sim.reset_meep()
    geometrys = [mp.Cylinder(material=Au,radius=r,center=mp.Vector3())]
    sim = mp.Simulation(cell_size=cell,
                    geometry=geometrys,
                    boundary_layers=pml_layers,
                    sources=sources,
                    resolution=resolution)
    
    lightside = sim.add_flux(fcen, df ,nfreq,lightside_fr)
    innerside = sim.add_flux(fcen, df ,nfreq,innerside_fr)
    otherside = sim.add_flux(fcen, df ,nfreq,otherside_fr)
    #sim.load_minus_flux_data(otherside,otherside_without_flux_data)
    sim.load_minus_flux_data(lightside,lightside_without_flux_data)
    sim.load_minus_flux_data(innerside,innerside_without_flux_data)
    pt = mp.Vector3(0.5*sx-dpml-0.01,0)
    sim.run(until_after_sources=mp.stop_when_fields_decayed(50,mp.Ez,pt,1e-1))
    a=mp.get_fluxes(lightside)
     #a=a[(74+12):(249-75+12)]
    lightside_with_flux = np.append(lightside_with_flux,a)
    a=mp.get_fluxes(otherside)
    #a=a[(74+12):(249-75+12)]
    
    otherside_with_flux = np.append(otherside_with_flux,a)
    innerside_with_flux = np.append(innerside_with_flux,mp.get_fluxes(innerside))
absorbtions = np.divide((otherside_with_flux-lightside_with_flux-2*innerside_with_flux),otherside_without_flux)#+np.divide(lightside_with_flux,otherside_without_flux)


wavelengths = np.linspace(800,400,100) 
plt.figure()
<<<<<<< HEAD
plt.plot(wavelengths,absorbtions[np.arange(0,100)],'r',label='absorbtion 20')
plt.plot(wavelengths,absorbtions[np.arange(100,200)],'g',label='absorbtion 40')
=======
plt.plot(wavelengths,apsorbtions[np.arange(0,100)],'r',label='absorbtion 5')
plt.plot(wavelengths,apsorbtions[np.arange(100,200)],'g',label='absorbtion 10')
plt.plot(wavelengths,apsorbtions[np.arange(200,300)],'b',label='absorbtion 15')
plt.plot(wavelengths,apsorbtions[np.arange(300,400)],'y',label='absorbtion 20')

>>>>>>> d91a969265bb9dadf409676e767cadad53e0d9fb

plt.legend(loc="upper left")
plt.grid()
plt.show()