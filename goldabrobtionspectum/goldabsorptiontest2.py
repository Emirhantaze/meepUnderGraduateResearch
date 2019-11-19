from __future__ import division
import meep as mp
import matplotlib.pyplot as plt
import numpy as np
import math
#from meep.materials import Au
pml_layers= [mp.PML(1)]
Au = mp.Medium(index=math.pow(6.9,(1/2)))
dpml=1
sx=7
cell = mp.Vector3(7,3)
minwavelength=0.4
maxwavelength=0.8
minf=1/maxwavelength
maxf=1/minwavelength
fcen = (maxf+minf)/2  
df = maxf-minf
nfreq=100
resolution = 40
sources = [mp.Source(mp.GaussianSource(fcen,fwidth=df),
                     component=mp.Ez,   
                     center=mp.Vector3(-2.5,0,0),
                     size=mp.Vector3(0,0.5,0))]
lightside_without_flux = []
otherside_without_flux = []
upperside_without_flux = []
lightside_with_flux = []
otherside_with_flux = []
upperside_with_flux = []
for i in (np.arange(1,6)):
    r=i*0.02
    sim = mp.Simulation(cell_size=cell,
                    boundary_layers=pml_layers,
                    sources=sources,
                    resolution=resolution)
    lightside_fr = mp.FluxRegion(center=mp.Vector3(-0.5-r), 
                             size=mp.Vector3(0,1,0))
    lightside = sim.add_flux(fcen, df ,nfreq,lightside_fr)
    otherside_fr = mp.FluxRegion(center=mp.Vector3(+0.5+r), 
                             size=mp.Vector3(0,1,0))
    otherside = sim.add_flux(fcen, df ,nfreq,otherside_fr)
    upperside_fr = mp.FluxRegion(center=mp.Vector3(0,0.49),
                                    size=mp.Vector3(1,0,0)) 
    upperside = sim.add_flux(fcen,df,nfreq,upperside_fr)
    pt = mp.Vector3(0.5*sx-dpml-0.5,0)
    sim.run(until_after_sources=mp.stop_when_fields_decayed(50,mp.Ez,pt,1e-3))
    lightside_without_flux = np.append(lightside_without_flux,mp.get_fluxes(lightside))
    otherside_without_flux = np.append(otherside_without_flux,mp.get_fluxes(otherside))
    upperside_without_flux = np.append(upperside_without_flux,mp.get_fluxes(upperside))
    sim.reset_meep()
    geometrys = [mp.Cylinder(material=Au,radius=r,center=mp.Vector3())]
    sim = mp.Simulation(cell_size=cell,
                    geometry=geometrys,
                    boundary_layers=pml_layers,
                    sources=sources,
                    resolution=resolution)
    lightside_fr = mp.FluxRegion(center=mp.Vector3(-0.5-r), 
                             size=mp.Vector3(0,1,0))
    lightside = sim.add_flux(fcen, df ,nfreq,lightside_fr)
    otherside_fr = mp.FluxRegion(center=mp.Vector3(+0.5+r), 
                             size=mp.Vector3(0,1,0))
    otherside = sim.add_flux(fcen, df ,nfreq,otherside_fr)
    upperside_fr = mp.FluxRegion(center=mp.Vector3(0,0.49),
                                    size=mp.Vector3(1,0,0)) 
    upperside = sim.add_flux(fcen,df,nfreq,upperside_fr)
    pt = mp.Vector3(0.5*sx-dpml-0.5,0)
    sim.run(until_after_sources=mp.stop_when_fields_decayed(50,mp.Ez,pt,1e-1))
    lightside_with_flux = np.append(lightside_with_flux,mp.get_fluxes(lightside))
    otherside_with_flux = np.append(otherside_with_flux,mp.get_fluxes(otherside))
    upperside_with_flux = np.append(upperside_with_flux,mp.get_fluxes(upperside))
apsorbtions = (otherside_without_flux-otherside_with_flux)-(lightside_without_flux-lightside_with_flux)-(upperside_without_flux-upperside_with_flux)
apsorbtions[np.arange(0,100)]=(apsorbtions[np.arange(0,100)]/(np.max(apsorbtions[np.arange(0,100)])))
apsorbtions[np.arange(100,200)]=(apsorbtions[np.arange(100,200)]/(np.max(apsorbtions[np.arange(100,200)])))
apsorbtions[np.arange(200,300)]=(apsorbtions[np.arange(200,300)]/(np.max(apsorbtions[np.arange(200,300)])))
apsorbtions[np.arange(300,400)]=(apsorbtions[np.arange(300,400)]/(np.max(apsorbtions[np.arange(300,400)])))
apsorbtions[np.arange(400,500)]=(apsorbtions[np.arange(400,500)]/(np.max(apsorbtions[np.arange(400,500)])))
wavelengths = np.linspace(800,400,100) 
plt.figure()
plt.plot(wavelengths,apsorbtions[np.arange(0,100)],'r',label='absorbtion 20')
plt.plot(wavelengths,apsorbtions[np.arange(100,200)],'g',label='absorbtion 40')
plt.plot(wavelengths,apsorbtions[np.arange(200,300)],'b',label='absorbtion 60')
plt.plot(wavelengths,apsorbtions[np.arange(300,400)],'y',label='absorbtion 80')
plt.plot(wavelengths,apsorbtions[np.arange(400,500)],'p',label='absorbtion 100')
plt.legend(loc="upper right")
plt.show()