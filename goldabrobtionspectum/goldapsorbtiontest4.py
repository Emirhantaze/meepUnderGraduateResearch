from __future__ import division
import meep as mp
import numpy as np
import matplotlib.pyplot as plt
import math
from meep.materials import Au

pml_layers=[mp.PML(0.4)]

#Au = mp.Medium(index=math.pow(6.9,(1/2)))
dpml=0.4
minwavelength=0.4
maxwavelength=0.8
minf=1/maxwavelength
maxf=1/minwavelength
fcen = (maxf+minf)/2  
df = maxf-minf
nfreq=100
resolution = 100


upperside_without_flux = []
otherside_without_flux = []
upperside_with_flux = []
lightside_with_flux = []
otherside_with_flux = []
indecentflux = []

for i in (np.arange(1,5)):
    r=i*0.005
    sx=12*r+2*dpml
    cell = mp.Vector3(sx,sx)
    sources = [mp.Source(mp.GaussianSource(fcen,fwidth=df),
                     component=mp.Ez,   
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
    upperside_fr = mp.FluxRegion(center=mp.Vector3(0,2*r), 
                             size=mp.Vector3(4*r,0,0),
                             )
    incedent_fr = mp.FluxRegion(center=mp.Vector3(0.5*sx-dpml-0.01),size= mp.Vector3(0,sx))
    incedent = sim.add_flux(fcen, df ,nfreq,incedent_fr)
    upperside = sim.add_flux(fcen, df ,nfreq,upperside_fr)
    pt = mp.Vector3(0.5*sx-dpml-0.01,0)
    sim.run(until_after_sources=mp.stop_when_fields_decayed(50,mp.Ez,pt,1e-9))
    lightside_without_flux_data = sim.get_flux_data(lightside)
    upperside_without_flux_data = sim.get_flux_data(upperside)
    otherside_without_flux_data= sim.get_flux_data(otherside)
    indecentflux = np.append(indecentflux,mp.get_fluxes(incedent))
    a=mp.get_fluxes(otherside)
    #a=a[(74+12):(249-75+12)]
    otherside_without_flux = np.append(otherside_without_flux,a)
    upperside_without_flux = np.append(upperside_without_flux,mp.get_fluxes(upperside))
    sim.reset_meep()
    geometrys = [mp.Cylinder(material=Au,radius=r,center=mp.Vector3())]
    sim = mp.Simulation(cell_size=cell,
                    geometry=geometrys,
                    boundary_layers=pml_layers,
                    sources=sources,
                    resolution=resolution)
    
    lightside = sim.add_flux(fcen, df ,nfreq,lightside_fr)
    upperside = sim.add_flux(fcen, df ,nfreq,upperside_fr)
    otherside = sim.add_flux(fcen, df ,nfreq,otherside_fr)
    #sim.load_minus_flux_data(otherside,otherside_without_flux_data)
    #sim.load_minus_flux_data(lightside,lightside_without_flux_data)
    #sim.load_minus_flux_data(upperside,upperside_without_flux_data)
    pt = mp.Vector3(0.5*sx-dpml-0.01,0)
    sim.run(until_after_sources=mp.stop_when_fields_decayed(50,mp.Ez,pt,1e-9))
    
    a=mp.get_fluxes(lightside)
     #a=a[(74+12):(249-75+12)]
    lightside_with_flux = np.append(lightside_with_flux,a)
    a=mp.get_fluxes(otherside)
    #a=a[(74+12):(249-75+12)]
    
    otherside_with_flux = np.append(otherside_with_flux,a)
    upperside_with_flux = np.append(upperside_with_flux,mp.get_fluxes(upperside))
apsorbtions = np.divide((otherside_with_flux-lightside_with_flux-2*upperside_with_flux),otherside_without_flux)#+np.divide(lightside_with_flux,otherside_without_flux)


wavelengths = np.linspace(800,400,100) 
plt.figure()
plt.plot(wavelengths,apsorbtions[np.arange(0,100)],'r',label='absorbtion 5')
plt.plot(wavelengths,apsorbtions[np.arange(100,200)],'g',label='absorbtion 10')
plt.plot(wavelengths,apsorbtions[np.arange(200,300)],'b',label='absorbtion 15')
plt.plot(wavelengths,apsorbtions[np.arange(300,400)],'y',label='absorbtion 20')


plt.legend(loc="upper right")
plt.show()