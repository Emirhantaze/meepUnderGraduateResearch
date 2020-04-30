import matplotlib.pyplot as plt
import meep as mp
import numpy as np
from meep.materials import Au
# while doing convergence test 
difference = 50
resolution = 500- difference
iscontinue = True
isfirstrun = True
oldtransmittiance = None
oldresolution=0

while iscontinue:
    wvl_min = 0.350
    wvl_max = 0.750
    frq_min = 1/wvl_max
    frq_max = 1/wvl_min
    frq_cen = 0.5*(frq_min+frq_max)
    dfrq = frq_max-frq_min
    nfrq = 100
    Material= Au
    resolution = resolution + difference
    dpml = 0.11
    pml_layers = [mp.PML(dpml, direction=mp.X, side=mp.High),
                        mp.Absorber(dpml, direction=mp.X, side=mp.Low)]
    symmetries = [mp.Mirror(mp.Y)]
    offsetx = 0.01
    block_thicknessy = 0.5
    block_thicknessx = 0.02
    spacing_thickness = block_thicknessy*2# this varible is our main purpose of doing this experiment
    celly = (spacing_thickness+block_thicknessy)
    cellx = block_thicknessx+2*dpml+2*offsetx

    geometry=[]

    sources = [mp.Source(mp.GaussianSource(frq_cen,fwidth=dfrq),
                        center=mp.Vector3(-0.5*cellx+dpml),
                        size=mp.Vector3(0,celly),
                        component=mp.Ez)]
    sim = mp.Simulation(resolution=resolution,
                        symmetries=symmetries,
                        cell_size=mp.Vector3(cellx,celly),
                        dimensions=3,
                        boundary_layers=pml_layers,
                        sources=sources,
                        ensure_periodicity=True,
                        k_point=mp.Vector3())

    transmittance_first_fr = mp.FluxRegion(center=mp.Vector3(0.5*cellx-dpml,0,0),size=mp.Vector3(0,celly))
    transmittance_first = sim.add_flux(frq_cen,dfrq,nfrq,transmittance_first_fr)
    pt = mp.Vector3(0.5*cellx-dpml,0,0)

    sim.run(until_after_sources=100)

    transmittance_first_flux =  mp.get_fluxes(transmittance_first)
    flux_freqs = mp.get_flux_freqs(transmittance_first)

    sim.reset_meep()
    geometry=[mp.Block(mp.Vector3(block_thicknessx,block_thicknessy,mp.inf),
                        center=mp.Vector3(),
                        material=Material)]
    pt = mp.Vector3(0.5*cellx-dpml,0,0)
    sim = mp.Simulation(resolution=resolution,
                        symmetries=symmetries,
                        cell_size=mp.Vector3(cellx,celly),
                        boundary_layers=pml_layers,
                        sources=sources,
                        k_point=mp.Vector3(),
                        ensure_periodicity=True,
                        geometry=geometry)

    transmittance_first = sim.add_flux(frq_cen,dfrq,nfrq,transmittance_first_fr)
    sim.run(until_after_sources=100)
    transmittance_second_flux =  mp.get_fluxes(transmittance_first)

    transmittance_ratio=np.divide(np.asarray(transmittance_second_flux),np.asarray(transmittance_first_flux))
    wvls=np.divide(1,np.asarray(flux_freqs))
    if isfirstrun:
        """
        plt.plot(wvls,transmittance_ratio , color="r",label=f'resolution: {resolution}')
        plt.legend()
        plt.show()
        """
        sim.plot2D()
        plt.show()
        isfirstrun = False
        oldtransmittiance=transmittance_ratio
        oldresolution=resolution
    else: 
        diff= np.sum(np.abs(np.subtract(oldtransmittiance,transmittance_ratio)))
        plt.title(f'diff: {diff}')
        plt.plot(wvls,oldtransmittiance , color="black",label=f'resolution: {oldresolution}')
        plt.plot(wvls,transmittance_ratio , color="r",label=f'resolution: {resolution}')
        oldtransmittiance=transmittance_ratio
        if(diff<0.05):
            iscontinue=False
        else:
            oldresolution=resolution
        plt.legend()
        plt.show()
        pass
print(f"Convergence Test is finished resolution should be: {oldresolution}")