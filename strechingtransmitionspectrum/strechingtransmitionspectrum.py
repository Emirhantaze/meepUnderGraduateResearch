import matplotlib.pyplot as plt
import meep as mp
import numpy as np
from meep.materials import Au
from datetime import datetime

difference = 1
setdiferrence = 1
iscontinue = True
iterator= 1 
lastitereation=5
while iscontinue:
    wvl_min = 0.150
    wvl_max = 0.950
    frq_min = 1/wvl_max
    frq_max = 1/wvl_min
    frq_cen = 0.5*(frq_min+frq_max)
    dfrq = frq_max-frq_min
    nfrq = 100
    Material= Au
    resolution = 300
    dpml = 0.11
    pml_layers = [mp.PML(dpml, direction=mp.X, side=mp.High),
                        mp.Absorber(dpml, direction=mp.X, side=mp.Low)]
    symmetries = [mp.Mirror(mp.Y)]
    offsetx = 0.05
    block_thicknessy = 0.5
    block_thicknessx = 0.02
    spacing_thickness = block_thicknessy*setdiferrence#

    celly = (spacing_thickness+block_thicknessy)
    cellx = block_thicknessx+2*dpml+2*offsetx

    geometry=[]

    sources = [mp.Source(mp.GaussianSource(frq_cen,fwidth=dfrq),
                        center=mp.Vector3(-0.5*cellx+dpml),
                        size=mp.Vector3(0,celly),
                        component=mp.Ey)]
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
    # transmittance_ratio = np.asarray(transmittance_second_flux)
    # transmittance_ratio=transmittance_ratio-np.mean(transmittance_ratio)
    wvls=np.multiply(np.divide(1,np.asarray(flux_freqs)),1000)
    plt.plot(wvls,transmittance_ratio,color=f"C{iterator}",label=f"spacing_thickness:{spacing_thickness}")
    setdiferrence+=difference
    if(iterator==lastitereation):
        iscontinue=False
    else:
        iterator+=1
plt.title(f"transmissionToWavelengths")
plt.xlabel("wavelengths")
plt.ylabel("transmission")
time = datetime.now().strftime("%d-%m-%Y_%I-%M-%S_%p")
name = __file__.split("/")
name=name[len(name)-1]
plt.legend()
plt.show()
# plt.savefig(fname=f"/home/emirhan/meepUnderGraduateResearch/pictures/{name}-{time}.svg",format="svg")
