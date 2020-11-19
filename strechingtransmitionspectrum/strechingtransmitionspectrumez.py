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
    for j in [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1]:
        ORAN = j

        guess = []
        if(ORAN == 0.1):
            # for 0.1 portion

            guess = [9.77423308e-02, 1.00000000e-10, 8.97862938e-01, 1.00000000e-10,
                     4.82050659e+01, 1.82514496e+02, 6.88382384e+01, 1.52658236e+00,
                     3.68995631e-01, 1.53942725e+02, 2.18405623e+00, 5.75401154e-01,
                     1.59761743e+02, 3.24374033e+00, 9.79274650e-01, 9.93593909e+00,
                     1.66697557e+02, 2.76735037e+01, 2.49933040e+00]
        elif(ORAN == 0.2):
            # for 0.2 portion

            guess = [1.30629985e-01, 2.26319869e+02, 1.00000000e-10, 2.17263249e-07,
                     3.00000000e+01, 1.82514496e+02, 2.69231977e+02, 1.40201548e+00,
                     8.60991162e-01, 5.63111849e+01, 2.17220096e+00, 5.41502956e-01,
                     1.63446009e+02, 3.19364529e+00, 9.86096525e-01, 9.91367717e+00,
                     2.99862012e+01, 2.76591242e+01, 3.30711256e+00]
        elif(ORAN == 0.3):

            # for 0.3 portion
            guess = [2.23407973e-01,  5.14792781e+02,  2.20610555e+00,  1.00000000e-10,
                     -1.19048744e+01,  4.52785777e+02,  1.00000000e-10,  3.84765045e-07,
                     9.48874754e+01,  8.59917093e+00,  3.12400116e+00,  2.30285986e-01,
                     1.00000000e-10,  6.19764794e+00,  4.16376252e+00,  1.00000000e-10,
                     1.81777663e+01,  1.46038634e+00,  3.84012808e+00]

        elif(ORAN == 0.4):

            # for 0.4 portion

            guess = [1.45281414e+00,  1.00000000e-10,  5.12707370e+00,  1.00000000e-10,
                     -5.75533172e-02,  9.07139969e+00,  9.76852212e+00,  7.78836820e-01,
                     1.75458771e+00,  1.00000000e-10,  2.95885460e+00,  1.98690451e+00,
                     9.50460986e-01,  3.01177484e+00,  5.27344514e-01,  7.40361572e+00,
                     3.82120021e+00,  1.00000000e-10,  1.00000000e+00]

        elif(ORAN == 0.5):

            # for 0.5 portion

            guess = [2.02098616e+00,  1.00000000e-10,  1.00379993e+01,  5.65291831e+00,
                     -2.01426547e-01,  7.40176922e-01,  6.32889402e+00,  3.31848610e+00,
                     1.00000000e-10,  6.01909241e-01,  2.05745883e+00,  9.56468570e-01,
                     9.46870604e-01,  3.11779840e+00,  6.31031437e-01,  2.04299862e-01,
                     2.76875969e+00,  3.83478456e-01,  1.00000000e+00]

        elif(ORAN == 0.6):
            # for 0.6 portion

            guess = [2.16259263e+00, 1.00000000e-10, 9.99864586e+00, 6.77999562e+00,
                     2.91732544e-06, 1.00000000e-10, 3.97279462e+00, 3.11071965e+00,
                     6.92561615e-01, 1.21718301e+00, 2.03876665e+00, 1.17459884e+00,
                     7.57142007e-01, 3.01937987e+00, 6.54834836e-01, 1.50265412e-01,
                     2.72111048e+00, 3.47122083e-01, 2.97199162e+00]

        elif(ORAN == 0.7):

            # for 0.7 portion

            guess = [7.89023859e-01,  1.00000000e-10,  1.67467932e+01,  4.98362208e+01,
                     -7.00431918e-01,  1.00000000e-10,  8.59155335e+00,  2.50397393e+00,
                     5.75035873e-01,  1.70582701e+00,  2.19646729e+00,  3.76670026e-01,
                     7.18336933e+00,  2.73208824e+00,  6.57561460e-01,  2.89820785e+01,
                     3.69075060e+00,  1.00000000e-10,  1.00000000e+00]

        elif(ORAN == 0.8):

            # for 0.8 portion

            guess = [2.20952072e+00, 1.00000000e-10, 3.08307514e+00, 1.30451977e+01,
                     8.66834886e-07, 1.00000000e-10, 1.00000000e-10, 1.58390897e+00,
                     2.45891641e-01, 1.00000000e-10, 4.55795528e-01, 5.61822309e+00,
                     1.33127364e+00, 2.78073316e+00, 7.51456359e-01, 2.23177537e+00,
                     3.33520907e+00, 7.08755770e-01, 5.84861626e+00]

        elif(ORAN == 0.9):

            # for 0.9 portion

            guess = [3.99837366e-01,  7.64489707e+00,  2.40469605e+00,  4.64672954e+02,
                     -1.17204935e-04,  8.70368299e-05,  4.00584260e+01,  2.37950237e+00,
                     6.66585589e-01,  1.40037739e-02,  2.74904798e+01,  1.83602964e+01,
                     1.11445924e+01,  2.66217030e+00,  3.96599205e-01,  9.80600767e+01,
                     3.51300897e+00,  6.53023813e-01,  5.39260635e+00]
        elif(ORAN == 1):

            # for 1 portion

            guess = [2.74596985e+00,  2.55454715e-01,  8.30476963e+00,  1.10151790e+01,
                     -2.39854301e-01,  1.00000000e-10,  9.30170074e-02,  2.10186777e+00,
                     2.44996696e-01,  4.24986161e+00,  3.73509890e+00,  1.00135561e+00,
                     2.49007699e-01,  2.76360724e+00,  3.71637890e-01,  6.68914595e-01,
                     3.00816822e+00,  5.91449138e-01,  4.46871264e+00]
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
with open('resultsoran1.json', 'w') as f:
    json.dump(sim_results, f)
    pass
