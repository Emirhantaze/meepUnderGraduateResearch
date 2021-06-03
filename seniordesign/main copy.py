import matplotlib.pyplot as plt
import meep as mp
from meep.simulation import at_every
import numpy as np
results = []
for j in range(1, 10):
    simruntime = 60

    CdSe = mp.Medium(index=2.52)
    Glass = mp.Medium(index=1.5)
    ZnO = mp.Medium(index=2.21)

    celly = 4
    fingersize = 0.05*j

    cell = mp.Vector3(7.5, celly)
    polarization = mp.Ez
    pml_layers = [mp.Absorber(1, mp.X, mp.Low), mp.PML(1, mp.X, mp.High)]

    resolution = 80

    sources = [mp.Source(mp.ContinuousSource(wavelength=0.550, end_time=20),
                         component=polarization,
                         center=mp.Vector3(-1.5, 0))]

    # sources.append(mp.Source(mp.ContinuousSource(wavelength=0.550, end_time=20),
    #                          component=polarization,
    #                          center=mp.Vector3(-1.6, 3)))

    # sources.append(mp.Source(mp.ContinuousSource(wavelength=0.550, end_time=20),
    #                          component=polarization,
    #                          center=mp.Vector3(-1.4, -2)))

    firstfr = mp.FluxRegion(center=mp.Vector3(
        -2.25, 0, 0), size=mp.Vector3(0, celly))

    secfr = mp.FluxRegion(center=mp.Vector3(
        2.25, 0, 0), size=mp.Vector3(0, celly))

    sim = mp.Simulation(cell_size=cell,
                        k_point=mp.Vector3(),
                        default_material=CdSe,
                        boundary_layers=pml_layers,
                        ensure_periodicity=True,
                        geometry=[],
                        sources=sources,
                        resolution=resolution)

    before_block = sim.add_flux(1/0.550, 0.5, 5, secfr)

    # sim.plot2D(eps_parameters={"cmap": "brg"}, boundary_parameters={
    #     'hatch': 'o', 'linewidth': 1.5, 'facecolor': 'y', 'edgecolor': 'y', 'alpha': 0.7})

    sim.run(until=simruntime)
    # plt.show()

    before_block_flux = mp.get_fluxes(before_block)
    before_block_flux_data = sim.get_flux_data(before_block)
    flux_freqs = mp.get_flux_freqs(before_block)

    sim.reset_meep()
    # glass substrate
    geometry = [mp.Block(mp.Vector3(1, celly, mp.inf),
                         center=mp.Vector3(-2.25),
                         material=mp.Medium(index=1.6))]

    #  cadmium selineid QD
    geometry.append(mp.Block(mp.Vector3(0.5, celly),
                             center=mp.Vector3(-1.5), material=CdSe))

    numberof = int(celly//(2*fingersize))+1

    # zno layer
    for i in range(numberof):
        geometry.append(mp.Block(mp.Vector3(2, fingersize),
                                 center=mp.Vector3(-0.25, (celly/2)+fingersize-(2 * fingersize)*(i+1)), material=ZnO))

    sim = mp.Simulation(cell_size=cell,
                        k_point=mp.Vector3(),
                        ensure_periodicity=True,
                        boundary_layers=pml_layers,
                        geometry=geometry,
                        sources=sources,
                        resolution=resolution)

    after_block = sim.add_flux(1/0.550, 0.5, 5, secfr)
    before_block = sim.add_flux(1/0.550, 0.5, 5, firstfr)

    sim.load_minus_flux_data(before_block, before_block_flux_data)
    # animate = mp.Animate2D(sim,
    #                        labels=True,
    #                        fields=polarization,
    #                        realtime=True,
    #                        field_parameters={
    #                            'alpha': 0.8, 'cmap': 'RdBu', 'interpolation': 'none'},
    #                        boundary_parameters={'hatch': 'o', 'linewidth': 1.5, 'facecolor': 'y', 'edgecolor': 'b', 'alpha': 0.3})
    sim.run(until=simruntime)

    fig, ax = plt.subplots(1, 1)
    sim.plot2D(ax,  eps_parameters={"cmap": "brg"}, boundary_parameters={
        'hatch': 'o', 'linewidth': 1.5, 'facecolor': 'y', 'edgecolor': 'y', 'alpha': 0.7})

    after_block_flux_second_run = mp.get_fluxes(after_block)
    before_block_flux_second_run = mp.get_fluxes(before_block)
    # plt.savefig("a.svg")
    # animate.to_mp4(5, f"fingersize {fingersize}.mp4")
    print(
        f"transmittance is {(np.array(after_block_flux_second_run)/np.array(before_block_flux))[2]}")
    results.append((np.array(after_block_flux_second_run) /
                    np.array(before_block_flux))[2])
np.savetxt("./seniordesign/results.txt", results)
