import meep as mp
import numpy as np
import matplotlib.pyplot as plt
from meep.materials import Au
wvl_min = 0.350
wvl_max = 0.750
frq_min = 1/wvl_max
frq_max = 1/wvl_min
frq_cen = 0.5*(frq_min+frq_max)
dfrq = frq_max-frq_min
nfrq = 100
#here the resulation can be effect according to wavelength and simulation size
resolution = 100
dpml = 0.5*wvl_max
pml_layers = [mp.PML(thickness=dpml)]
block_number = 10 # here this number determines how many dielectric material has been used
block_thickness = wvl_max/10#thickness of each block
spacing_thickness = block_thickness*20# this varible is our main purpose of doing this experiment
celly = wvl_max*1 + dpml*2
cellx = 2*dpml+(block_number)*(spacing_thickness+block_thickness)+wvl_max/4
geometry=[]

sources = [mp.Source(mp.GaussianSource(frq_cen,fwidth=dfrq),
                    center=mp.Vector3(-0.5*cellx+dpml),
                    size=mp.Vector3(0,celly),
                    component=mp.Ez)]
sim = mp.Simulation(resolution=resolution,
                    cell_size=mp.Vector3(cellx,celly),
                    boundary_layers=pml_layers,
                    sources=sources,
                    k_point=mp.Vector3())

transmittance_first_fr = mp.FluxRegion(center=mp.Vector3(0.5*cellx-dpml-wvl_max*0.5,0,0),size=mp.Vector3(0,celly/2))
transmittance_first = sim.add_flux(frq_cen,dfrq,nfrq,transmittance_first_fr)
pt = mp.Vector3(0.5*cellx-dpml,0,0)

sim.run(until_after_sources=mp.stop_when_fields_decayed(50,mp.Ez,pt,1e-3))
eps_data = sim.get_array(center=mp.Vector3(), size=mp.Vector3(cellx,celly), component=mp.Dielectric)
ez_data = sim.get_array(center=mp.Vector3(), size=mp.Vector3(cellx,celly), component=mp.Ez)
plt.figure()
plt.imshow(eps_data.transpose(), interpolation='spline36', cmap='binary')
plt.axis('off')
plt.show()
plt.imshow(ez_data.transpose(), interpolation='spline36', cmap='RdBu', alpha=0.9)
plt.axis('off')
plt.show()
transmittance_first_flux =  mp.get_fluxes(transmittance_first)
flux_freqs = mp.get_flux_freqs(transmittance_first)
sim.reset_meep()
for i in range(block_number):
    geometry.append(mp.Block(mp.Vector3(block_thickness,celly,mp.inf),
                    center=mp.Vector3(((i+1)*(spacing_thickness+block_thickness)+block_thickness/2)+wvl_max/2-cellx/2),
                    material=Au))

pt = mp.Vector3(0.5*cellx-dpml,0,0)
sim = mp.Simulation(resolution=resolution,
                    cell_size=mp.Vector3(cellx,celly),
                    boundary_layers=pml_layers,
                    sources=sources,
                    k_point=mp.Vector3(),
                    geometry=geometry)
transmittance_first = sim.add_flux(frq_cen,dfrq,nfrq,transmittance_first_fr)
sim.run(until_after_sources=mp.stop_when_fields_decayed(50,mp.Ez,pt,1e-3))
transmittance_second_flux =  mp.get_fluxes(transmittance_first)

transmittance_ratio=np.divide(np.asarray(transmittance_second_flux),np.asarray(transmittance_first_flux))
wvls=np.divide(1,np.asarray(flux_freqs))
plt.plot(wvls,transmittance_ratio)
plt.show()
eps_data = sim.get_array(center=mp.Vector3(), size=mp.Vector3(cellx,celly), component=mp.Dielectric)
ez_data = sim.get_array(center=mp.Vector3(), size=mp.Vector3(cellx,celly), component=mp.Ez)
plt.figure()
plt.imshow(eps_data.transpose(), interpolation='spline36', cmap='binary')
plt.axis('off')
plt.show()
plt.imshow(ez_data.transpose(), interpolation='spline36', cmap='RdBu', alpha=0.9)
plt.axis('off')
plt.show()

