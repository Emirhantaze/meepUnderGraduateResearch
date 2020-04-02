import matplotlib.pyplot as plt
import meep as mp
import numpy as np
from meep.materials import Au

wvl_min = 0.350
wvl_max = 0.750
frq_min = 1/wvl_max
frq_max = 1/wvl_min
frq_cen = 0.5*(frq_min+frq_max)
dfrq = frq_max-frq_min
nfrq = 100
Material= Au
#here the resulation can be effect according to wavelength and simulation size
resolution = 50
dpml = 4*wvl_max
pml_layers = [mp.PML(dpml, direction=mp.X, side=mp.High),
                       mp.Absorber(dpml, direction=mp.X, side=mp.Low)]
symmetries = [mp.Mirror(mp.X)]
block_thicknessy = 0.5
block_thicknessx = 0.02
spacing_thickness = block_thicknessy*2# this varible is our main purpose of doing this experiment
celly = (spacing_thickness+block_thicknessy)
cellx = block_thicknessx+2*dpml
geometry=[]

sources = [mp.Source(mp.GaussianSource(frq_cen,fwidth=dfrq),
                    center=mp.Vector3(-0.5*cellx+dpml),
                    size=mp.Vector3(0,celly),
                    component=mp.Ex)]
sim = mp.Simulation(resolution=resolution,
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
box_x1_data = sim.get_flux_data(transmittance_first)
flux_freqs = mp.get_flux_freqs(transmittance_first)
sim.reset_meep()
"""
for i in range(block_number):
    geometry.append(mp.Block(mp.Vector3(block_thickness*4,block_thickness,mp.inf),
                    center=mp.Vector3(0,((i+1)*(spacing_thickness+block_thickness)+block_thickness/2)+celly/2),
                    material=Material))
"""
geometry=[mp.Block(mp.Vector3(block_thicknessx,block_thicknessy,mp.inf),
                    center=mp.Vector3(),
                    material=Material)]
pt = mp.Vector3(0.5*cellx-dpml,0,0)
sim = mp.Simulation(resolution=resolution,
                    cell_size=mp.Vector3(cellx,celly),
                    boundary_layers=pml_layers,
                    sources=sources,
                    k_point=mp.Vector3(),
                    ensure_periodicity=True,
                    geometry=geometry)
transmittance_first = sim.add_flux(frq_cen,dfrq,nfrq,transmittance_first_fr)
sim.load_minus_flux_data(transmittance_first, box_x1_data)
sim.run(until_after_sources=100)
transmittance_second_flux =  mp.get_fluxes(transmittance_first)

transmittance_ratio=np.divide(np.asarray(transmittance_second_flux),np.asarray(transmittance_first_flux))
wvls=np.divide(1,np.asarray(flux_freqs))
plt.plot(wvls,np.asarray(transmittance_first_flux))
plt.show()
