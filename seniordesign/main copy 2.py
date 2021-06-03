import meep as mp
import numpy as np
results = []
for fi in range(1):
    for fj in range(10):

        fingersize = 0.05*(fj+1)
        cell = mp.Vector3(7, fingersize*10, fingersize*10)
        pml_layers = [mp.Absorber(1, mp.X, mp.Low), mp.PML(1, mp.X, mp.High)]
        CdSe = mp.Medium(index=2.52)
        ZnO = mp.Medium(index=2.21)
        resolution = 80-fj*4

        sources = [mp.Source(mp.ContinuousSource(wavelength=0.550, end_time=10),
                             component=mp.Ez,
                             center=mp.Vector3(-1, 0, 0))]

        firstfr = mp.FluxRegion(center=mp.Vector3(
            -2, 0, 0), size=mp.Vector3(0, cell.y, cell.z))

        secfr = mp.FluxRegion(center=mp.Vector3(
            2.5, 0, 0), size=mp.Vector3(0, cell.y, cell.z))

        sim = mp.Simulation(cell_size=cell,
                            k_point=mp.Vector3(),
                            default_material=CdSe,
                            boundary_layers=pml_layers,
                            eps_averaging=False,
                            geometry=[],
                            ensure_periodicity=True,
                            sources=sources,
                            dimensions=3,
                            resolution=resolution)

        before_block = sim.add_flux(1/0.550, 0.5, 5, secfr)

        sim.run(until=60)

        before_block_flux = mp.get_fluxes(before_block)
        before_block_flux_data = sim.get_flux_data(before_block)
        flux_freqs = mp.get_flux_freqs(before_block)

        sim.reset_meep()

        geometry = [mp.Block(mp.Vector3(1, cell.y, cell.z),
                             center=mp.Vector3(-2),
                             material=mp.Medium(index=1.6))]
        #  cadmium selineid QD
        geometry.append(mp.Block(mp.Vector3(1, cell.z, cell.z),
                                 center=mp.Vector3(-1), material=mp.Medium(index=2.52)))

        numberof = int(cell.y//(2*fingersize))+1

        for i in range(numberof):
            for j in range(numberof):
                geometry.append(mp.Cylinder(height=1, radius=fingersize/2, axis=mp.Vector3(1, 0, 0),
                                            center=mp.Vector3(0, (cell.y/2)+fingersize-(2 * fingersize)*(i+1), (cell.z/2)+fingersize-(2 * fingersize)*(j+1)), material=ZnO))

        sources = [mp.Source(mp.ContinuousSource(wavelength=0.550, end_time=10),
                             component=mp.Ez,
                             center=mp.Vector3(-1, 0, 0))]

        sim = mp.Simulation(cell_size=cell,
                            k_point=mp.Vector3(),
                            boundary_layers=pml_layers,
                            geometry=geometry,
                            dimensions=3,
                            eps_averaging=False,
                            ensure_periodicity=True,
                            sources=sources,
                            resolution=resolution)

        after_block = sim.add_flux(1/0.550, 0.5, 5, secfr)
        before_block = sim.add_flux(1/0.550, 0.5, 5, firstfr)

        sim.load_minus_flux_data(before_block, before_block_flux_data)

        sim.run(until=60)

        after_block_flux_second_run = mp.get_fluxes(after_block)
        before_block_flux_second_run = mp.get_fluxes(before_block)

        print(
            f"transmittance is {(np.array(after_block_flux_second_run)/np.array(before_block_flux))[2]}")
        results.append((np.array(after_block_flux_second_run) /
                        np.array(before_block_flux))[2])
        np.savetxt(f"QD: {1} result.txt", results)
