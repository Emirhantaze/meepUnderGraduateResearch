from __future__ import division
from meep.materials import Au
import meep as mp
import matplotlib.pyplot as plt
import numpy as np

for j in np.arange(1.0,3.0,1.0):

    r=j*5
    pmlsize=0.5
    pml_layers = [mp.PML(pmlsize)]
    cxs=2*r+10
    cell = mp.Vector3(cxs,2*(r+pmlsize))
    resolution = 10 
    cwl=0.5
    ww=0.6

    sources = [mp.Source(mp.GaussianSource(wavelength=cwl,width=ww),
                        component=mp.Ez,
                        center=mp.Vector3(-(cxs/2)+2*pmlsize,0),
                        size=mp.Vector3(0)
                        )]
    sim = mp.Simulation(cell_size=cell,
                        boundary_layers=pml_layers,
                        sources=sources,
                        resolution=resolution)

    nfreq = 60

    refl_fr = mp.FluxRegion(center=mp.Vector3(-0.5*cxs+pmlsize+0.5,0,0),size=mp.Vector3(0,2*r,0))
    refl = sim.add_flux(1/cwl, 1/ww ,nfreq,refl_fr)

    tran_fr = mp.FluxRegion(center=mp.Vector3(0.5*cxs-pmlsize-0.5,0,0),size=mp.Vector3(0,2*r,0))
    tran = sim.add_flux(1/cwl, 1/ww ,nfreq,tran_fr)

    pt = mp.Vector3(0.5*cxs-pmlsize-0.5)

    sim.run(until_after_sources=mp.stop_when_fields_decayed(50,mp.Ez,pt,1e-3))

    # for normalization run, save flux fields data for reflection plane
    straight_refl_data = sim.get_flux_data(refl)

    # save incident power for transmission plane
    straight_tran_flux = mp.get_fluxes(tran)
    print(straight_tran_flux)
    sim.reset_meep()
    geometry = [mp.Cylinder(material=mp.Medium(index=6.9),radius=r,
                        center=mp.Vector3(0,0,0))]

    sim = mp.Simulation(cell_size=cell,
                        boundary_layers=pml_layers,
                        geometry=geometry,
                        sources=sources,
                        resolution=resolution)

    refl = sim.add_flux(1/cwl, 1/ww ,nfreq,refl_fr)

    tran_fr = mp.FluxRegion(center=mp.Vector3(0.5*cxs-pmlsize-0.5,0,0),size=mp.Vector3(0,2*r,0))
    tran = sim.add_flux(1/cwl, 1/ww ,nfreq,tran_fr)

    sim.load_minus_flux_data(refl,straight_refl_data)

    pt = mp.Vector3(0.5*cxs-pmlsize-0.5)
    sim.run(until_after_sources=mp.stop_when_fields_decayed(50,mp.Ez,pt,1e-3))
    bend_refl_flux = mp.get_fluxes(refl)
    bend_tran_flux = mp.get_fluxes(tran)
    flux_freqs = mp.get_flux_freqs(refl)
    print(bend_tran_flux)

    wl = []

    Ts = []
    for i in range(nfreq):
        wl = np.append(wl, (1/flux_freqs[i])*1000)
        
        
        Ts = np.append(Ts,-bend_tran_flux[i]+(straight_tran_flux[i]))

    if j==1:

        plt.figure()
    
        plt.plot(wl,Ts,'r',label='absorbtion')
        #plt.xticks(np.arange(0.3,0.9,0.04))
    
        
    elif j==2:
        
    
        plt.plot(wl,Ts,'g',label='absorbtion')
        

    else:
        if j==3:
            plt.plot(wl,Ts,'b',label='absorbtion')
        else:
            plt.plot(wl,Ts,'y',label='absorbtion')
plt.xlabel("wavelength (nm)")
plt.legend(loc="upper right")
plt.show()
