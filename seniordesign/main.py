import matplotlib.pyplot as plt
import meep as mp
import numpy as np

cell = mp.Vector3(10, 30)

pml_layers = [mp.Absorber(1, mp.X, mp.Low), mp.PML(1, mp.X, mp.High)]

resolution = 50

# glass substrate


sources = [mp.Source(mp.ContinuousSource(wavelength=0.450, end_time=20),
                     component=mp.Ez,
                     center=mp.Vector3(-3, 0))]

firstfr = mp.FluxRegion(center=mp.Vector3(
    -2, 0, 0), size=mp.Vector3(0, 30))

secfr = mp.FluxRegion(center=mp.Vector3(
    4, 0, 0), size=mp.Vector3(0, 30))

sim = mp.Simulation(cell_size=cell,
                    k_point=mp.Vector3(),
                    default_material=mp.Medium(index=1.6),
                    boundary_layers=pml_layers,
                    geometry=[],
                    sources=sources,
                    resolution=resolution)

before_block = sim.add_flux(1/0.450, 0.5, 5, firstfr)


sim.plot2D(eps_parameters={"cmap": "brg"}, boundary_parameters={
    'hatch': 'o', 'linewidth': 1.5, 'facecolor': 'y', 'edgecolor': 'y', 'alpha': 0.7})

sim.run(until=200)
plt.show()

before_block_flux = mp.get_fluxes(before_block)
before_block_flux_data = sim.get_flux_data(before_block)
flux_freqs = mp.get_flux_freqs(before_block)

sim.reset_meep()

geometry = [mp.Block(mp.Vector3(4, 30, mp.inf),
                     center=mp.Vector3(-3),
                     material=mp.Medium(index=1.6))]

#  cadmium selineid QD
geometry.append(mp.Block(mp.Vector3(1, 30),
                         center=mp.Vector3(-0.5), material=mp.Medium(index=2.52)))

# # ilel layer
# geometry.append(mp.Block(mp.Vector3(1, 30),
#                          center=mp.Vector3(0.5), material=mp.Medium(index=1.81)))

sources = [mp.Source(mp.ContinuousSource(wavelength=0.450, end_time=20),
                     component=mp.Ez,
                     center=mp.Vector3(-3, 0))]


sim = mp.Simulation(cell_size=cell,
                    k_point=mp.Vector3(),
                    boundary_layers=pml_layers,
                    geometry=geometry,
                    sources=sources,
                    resolution=resolution)


# animate = mp.Animate2D(sim,
#                        labels=True,
#                        fields=mp.Ez,
#                        realtime=True,
#                        field_parameters={
#                            'alpha': 0.8, 'cmap': 'RdBu', 'interpolation': 'none'},
#                        boundary_parameters={'hatch': 'o', 'linewidth': 1.5, 'facecolor': 'y', 'edgecolor': 'b', 'alpha': 0.3})
# mp.at_every(1, animate),


after_block = sim.add_flux(1/0.450, 0.5, 5, secfr)
before_block = sim.add_flux(1/0.450, 0.5, 5, firstfr)


fig, ax = plt.subplots(1, 1)
sim.plot2D(ax,  eps_parameters={"cmap": "brg"}, boundary_parameters={
           'hatch': 'o', 'linewidth': 1.5, 'facecolor': 'y', 'edgecolor': 'y', 'alpha': 0.7})

sim.load_minus_flux_data(before_block, before_block_flux_data)

sim.run(until=200)
plt.show()

after_block_flux_second_run = mp.get_fluxes(after_block)
before_block_flux_second_run = mp.get_fluxes(before_block)

print(
    f"transmittance is {(np.array(after_block_flux_second_run)/np.array(before_block_flux))[2]}")
