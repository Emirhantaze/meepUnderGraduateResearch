import json
import matplotlib.pyplot as plt
import meep as mp
import numpy as np
from meep.materials import Au as au
from datetime import datetime

"""
defining au 
"""
sim_results = {
    "EZ": {},
    "EY": {}
}
counter = 0
for k in [mp.Ez, mp.Ey]:
    for j in [[0.3, 0.3, 0.4], [0.2, 0.4, 0.4], [0.1, 0.5, 0.4], [0.33, 0.33, 0.33]]:
        ORAN = j

        guess = []
        if ORAN == [0.3, 0.3, 0.4]:
            guess = [2.74596985e+00,  2.55454715e-01,  8.30476963e+00,  1.10151790e+01,
                     -2.39854301e-01,  1.00000000e-10,  9.30170074e-02,  2.10186777e+00,
                     2.44996696e-01,  4.24986161e+00,  3.73509890e+00,  1.00135561e+00,
                     2.49007699e-01,  2.76360724e+00,  3.71637890e-01,  6.68914595e-01,
                     3.00816822e+00,  5.91449138e-01,  4.46871264e+00]

        elif ORAN == [0.2, 0.4, 0.4]:
            guess = [1.76786524e+00,  1.00000000e-10,  8.33725870e+00,  9.68959739e+00,
                     -1.44867174e-06,  1.00000000e-10,  9.21375928e-01,  1.63359288e+00,
                     8.67630698e-01,  1.71681825e-01,  3.14412746e+00,  3.92369086e-01,
                     2.90495692e+00,  2.84743876e+00,  1.37007077e+00,  9.17725815e+00,
                     4.43149085e+00,  1.00000000e-10,  1.00000000e+00]

        elif ORAN == [0.1, 0.5, 0.4]:
            guess = [1.99048577e+00,  1.00000000e-10,  8.33725864e+00,  7.89153695e+00,
                     -4.40112284e-06,  1.00000000e-10,  8.45802229e-02,  1.52371226e+00,
                     3.11184433e-01,  2.20459131e+00,  2.82909918e+00,  1.55843426e+00,
                     3.85779361e-01,  2.14175595e+00,  6.82043582e-01,  1.23341222e+01,
                     5.25780929e+00,  1.15229738e+00,  1.00000000e+00]

        elif ORAN == [0.33, 0.33, 0.33]:
            guess = [1.76786524e+00,  1.00000000e-10,  8.33725870e+00,  9.68959739e+00,
                     -1.44867174e-06,  1.00000000e-10,  9.21375928e-01,  1.63359288e+00,
                     8.67630698e-01,  1.71681825e-01,  3.14412746e+00,  3.92369086e-01,
                     2.90495692e+00,  2.84743876e+00,  1.37007077e+00,  9.17725815e+00,
                     4.43149085e+00,  1.00000000e-10,  1.00000000e+00]
        x = guess
        um_scale = 1.0
        # conversion factor for eV to 1/um [=1/hc]
        eV_um_scale = um_scale/1.23984193
        metal_range = mp.FreqRange(min=um_scale/0.7, max=um_scale/.3)
        Au_plasma_frq = x[0]*eV_um_scale

        Au_f0 = x[1]
        Au_frq0 = 1e-10
        Au_gam0 = x[2]*eV_um_scale
        Au_sig0 = Au_f0*Au_plasma_frq**2/Au_frq0**2

        Au_f1 = x[3]
        Au_frq1 = x[4]    # 0.42 um
        Au_gam1 = x[5]*eV_um_scale
        Au_sig1 = Au_f1*Au_plasma_frq**2/Au_frq1**2

        Au_f2 = x[6]
        Au_frq2 = x[7]  # 0.42 um
        Au_gam2 = x[8]*eV_um_scale
        Au_sig2 = Au_f2*Au_plasma_frq**2/Au_frq2**2
        Au_f3 = x[9]
        Au_frq3 = x[10]*eV_um_scale      # 0.418 um
        Au_gam3 = x[11]*eV_um_scale
        Au_sig3 = Au_f3*Au_plasma_frq**2/Au_frq3**2
        Au_f4 = x[12]
        Au_frq4 = x[13]*eV_um_scale      # 0.288 um
        Au_gam4 = x[14]*eV_um_scale
        Au_sig4 = Au_f4*Au_plasma_frq**2/Au_frq4**2
        Au_f5 = x[15]
        Au_frq5 = x[16]*eV_um_scale      # 0.093 um
        Au_gam5 = x[17]*eV_um_scale
        Au_sig5 = Au_f5*Au_plasma_frq**2/Au_frq5**2
        Au_susc = [mp.DrudeSusceptibility(frequency=Au_frq0, gamma=Au_gam0, sigma=Au_sig0),
                   mp.LorentzianSusceptibility(
            frequency=Au_frq1, gamma=Au_gam1, sigma=Au_sig1),
            mp.LorentzianSusceptibility(
            frequency=Au_frq2, gamma=Au_gam2, sigma=Au_sig2),
            mp.LorentzianSusceptibility(
            frequency=Au_frq3, gamma=Au_gam3, sigma=Au_sig3),
            mp.LorentzianSusceptibility(
            frequency=Au_frq4, gamma=Au_gam4, sigma=Au_sig4),
            mp.LorentzianSusceptibility(frequency=Au_frq5, gamma=Au_gam5, sigma=Au_sig5)]

        Au = mp.Medium(epsilon=x[18], E_susceptibilities=Au_susc)
        """
        """
        # from meep.materials import Au
        offsetx = 0.05
        block_thicknessy = 0.5 * 1
        block_thicknessx = 0.02
        spacing_thickness_orj = block_thicknessy
        iscontinue = True
        iterator = 0
        lastitereation = 3
        while iscontinue:
            counter += 1
            print("******************************")
            print("******************************")
            print("******************************")
            print(f"****    counter = {counter}     ******")
            print("******************************")
            print("******************************")
            print("******************************")

            spacing_thickness = spacing_thickness_orj + \
                spacing_thickness_orj*(iterator/lastitereation)
            wvl_min = 0.400
            wvl_max = 0.700
            frq_min = 1/wvl_max
            frq_max = 1/wvl_min
            frq_cen = 0.5*(frq_min+frq_max)
            dfrq = frq_max-frq_min
            nfrq = 100
            Material = Au
            resolution = 220
            dpml = 0.11
            pml_layers = [mp.Absorber(dpml, direction=mp.X, side=mp.High),
                          mp.Absorber(dpml, direction=mp.X, side=mp.Low)]
            if (k == mp.Ey):
                symmetries = [mp.Mirror(mp.Y, phase=-1)]
            else:
                symmetries = [mp.Mirror(mp.Y)]

            celly = (spacing_thickness+block_thicknessy)
            cellx = block_thicknessx+2*dpml+2*offsetx

            geometry = []

            sources = [mp.Source(mp.GaussianSource(frq_cen, fwidth=dfrq, is_integrated=True),
                                 center=mp.Vector3(-0.5*cellx+dpml+0.01),
                                 size=mp.Vector3(0, celly),
                                 component=k)]
            sim = mp.Simulation(resolution=resolution,
                                symmetries=symmetries,
                                cell_size=mp.Vector3(cellx, celly),
                                dimensions=3,
                                boundary_layers=pml_layers,
                                sources=sources,
                                ensure_periodicity=True,
                                k_point=mp.Vector3())

            after_block_fr = mp.FluxRegion(center=mp.Vector3(
                0.5*cellx-dpml-0.01, 0, 0), size=mp.Vector3(0, celly))
            before_block_fr = mp.FluxRegion(
                center=mp.Vector3(-0.5*cellx+dpml+0.02, 0, 0), size=mp.Vector3(0, celly))

            after_block = sim.add_flux(frq_cen, dfrq, nfrq, after_block_fr)
            before_block = sim.add_flux(frq_cen, dfrq, nfrq, before_block_fr)
            pt = mp.Vector3(0.5*cellx-dpml-0.01, 0, 0)

            sim.run(until_after_sources=mp.stop_when_fields_decayed(
                50, k, pt, 1e-3))

            after_block_flux = mp.get_fluxes(after_block)
            before_block_flux_data = sim.get_flux_data(before_block)
            flux_freqs = mp.get_flux_freqs(after_block)

            sim.reset_meep()
            geometry = [mp.Block(mp.Vector3(block_thicknessx, block_thicknessy, mp.inf),
                                 center=mp.Vector3(),
                                 material=Material)]
            sim = mp.Simulation(resolution=resolution,
                                symmetries=symmetries,
                                cell_size=mp.Vector3(cellx, celly),
                                boundary_layers=pml_layers,
                                sources=sources,
                                k_point=mp.Vector3(),
                                ensure_periodicity=True,
                                geometry=geometry,
                                )
            before_block = sim.add_flux(frq_cen, dfrq, nfrq, before_block_fr)

            after_block = sim.add_flux(frq_cen, dfrq, nfrq, after_block_fr)
            sim.load_minus_flux_data(before_block, before_block_flux_data)
            sim.run(until_after_sources=mp.stop_when_fields_decayed(
                50, k, pt, 1e-3))
            after_block_flux_second_run = mp.get_fluxes(after_block)
            before_block_flux_second_run = mp.get_fluxes(before_block)
            # np.savetxt(f"tra_ez_ST{round(spacing_thickness,2)}.txt",after_block_flux_second_run)
            # np.savetxt(f"ref_ez_ST{round(spacing_thickness,2)}.txt",before_block_flux_second_run)
            # np.savetxt(f"in_ez_ST{round(spacing_thickness,2)}.txt",after_block_flux)
            if(k == mp.Ez):
                if(iterator == 0):
                    sim_results["EZ"][f"Ratio_{ORAN}"] = {}
                    sim_results["EZ"][f"Ratio_{ORAN}"][f"Spacing_{round(spacing_thickness,2)}"] = {
                        "Transmission": list(after_block_flux_second_run),
                        "Reflected": list(before_block_flux_second_run),
                        "Incident": list(after_block_flux)
                    }
                else:
                    sim_results["EZ"][f"Ratio_{ORAN}"][f"Spacing_{round(spacing_thickness,2)}"] = {
                        "Transmission": list(after_block_flux_second_run),
                        "Reflected": list(before_block_flux_second_run),
                        "Incident": list(after_block_flux)
                    }
            else:
                if(iterator == 0):
                    sim_results["EY"][f"Ratio_{ORAN}"] = {}
                    sim_results["EY"][f"Ratio_{ORAN}"][f"Spacing_{round(spacing_thickness,2)}"] = {
                        "Transmission": list(after_block_flux_second_run),
                        "Reflected": list(before_block_flux_second_run),
                        "Incident": list(after_block_flux)
                    }
                else:
                    sim_results["EY"][f"Ratio_{ORAN}"][f"Spacing_{round(spacing_thickness,2)}"] = {
                        "Transmission": list(after_block_flux_second_run),
                        "Reflected": list(before_block_flux_second_run),
                        "Incident": list(after_block_flux)
                    }
            sim.reset_meep()
            if(iterator == lastitereation):
                iscontinue = False
            else:
                iterator += 1
sim_results["Other_Params"] = f"Resolution={resolution},BlockThicknessY={block_thicknessy},BlockThicknessX={block_thicknessx},PML={dpml},cellx={cellx},celly={celly}"
sim_results["Wavelengths"] = list(1/np.asarray(flux_freqs))
with open('silvergoldpolimer.json', 'w') as f:
    json.dump(sim_results, f)
    pass
