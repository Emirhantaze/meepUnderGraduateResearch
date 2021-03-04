import json
import matplotlib.pyplot as plt
import meep as mp
import numpy as np
from meep.materials import Au as au
from datetime import datetime
from numpy import load

# gold is 0
or0 = np.array([[0, 0, 0, 0], [0.2, 0.4, 0.6, 0.8], [0.8, 0.6, 0.4, 0.2]])
o9 = np.array([or0[::, 0], or0[::, 1], or0[::, 2], or0[::, 3]])

# gold is 0
or0 = np.array([[0.2, 0.4, 0.6, 0.8], [0, 0, 0, 0], [0.8, 0.6, 0.4, 0.2]])
o10 = np.array([or0[::, 0], or0[::, 1], or0[::, 2], or0[::, 3]])

# gold is 0
or0 = np.array([[0.2, 0.4, 0.6, 0.8], [0.8, 0.6, 0.4, 0.2], [0, 0, 0, 0]])
o11 = np.array([or0[::, 0], or0[::, 1], or0[::, 2], or0[::, 3]])

# only gold silver pdms

o12 = np.array([[0, 0, 1], [0, 1, 0], [1, 0, 0]])
# gold is 0.25 and others are changing
or0 = np.array([[0.25, 0.25, 0.25, 0.25], [
               0.15, 0.3, 0.45, 0.6], [0.6, 0.45, 0.3, 0.15]])
o0 = np.array([or0[::, 0], or0[::, 1], or0[::, 2], or0[::, 3]])
#silver is 0.25
or0 = np.array([[0.15, 0.3, 0.45, 0.6], [0.25, 0.25,
                                         0.25, 0.25], [0.6, 0.45, 0.3, 0.15]])
o1 = np.array([or0[::, 0], or0[::, 1], or0[::, 2], or0[::, 3]])
# pdms is 0.25
or0 = np.array([[0.15, 0.3, 0.45, 0.6], [0.6, 0.45,
                                         0.3, 0.15], [0.25, 0.25, 0.25, 0.25]])
o2 = np.array([or0[::, 0], or0[::, 1], or0[::, 2], or0[::, 3]])

# gold is 0.5
or0 = np.array(
    [[0.5, 0.5, 0.5, 0.5], [0.1, 0.2, 0.3, 0.4], [0.4, 0.3, 0.2, 0.1]])
o3 = np.array([or0[::, 0], or0[::, 1], or0[::, 2], or0[::, 3]])
# silver is 0.5
or0 = np.array(
    [[0.1, 0.2, 0.3, 0.4], [0.5, 0.5, 0.5, 0.5], [0.4, 0.3, 0.2, 0.1]])
o4 = np.array([or0[::, 0], or0[::, 1], or0[::, 2], or0[::, 3]])
# pdms 0.5
or0 = np.array(
    [[0.1, 0.2, 0.3, 0.4], [0.4, 0.3, 0.2, 0.1], [0.5, 0.5, 0.5, 0.5]])
o5 = np.array([or0[::, 0], or0[::, 1], or0[::, 2], or0[::, 3]])

#gold is 0.75
or0 = np.array([[0.75, 0.75, 0.75, 0.75], [
               0.05, 0.1, 0.15, 0.2], [0.2, 0.15, 0.1, 0.05]])
o6 = np.array([or0[::, 0], or0[::, 1], or0[::, 2], or0[::, 3]])
# silver is 0.75
or0 = np.array([[0.05, 0.1, 0.15, 0.2], [0.75, 0.75,
                                         0.75, 0.75], [0.2, 0.15, 0.1, 0.05]])
o7 = np.array([or0[::, 0], or0[::, 1], or0[::, 2], or0[::, 3]])
# pdms is 0.75
or0 = np.array([[0.05, 0.1, 0.15, 0.2], [0.2, 0.15,
                                         0.1, 0.05], [0.75, 0.75, 0.75, 0.75]])
o8 = np.array([or0[::, 0], or0[::, 1], or0[::, 2], or0[::, 3]])
o = [o0, o1, o2, o3, o4, o5, o6, o7, o8, o9, o10, o11]

o = np.reshape(o, (np.int(np.size(o)/3), 3))
o = np.append(o, o12)
o = np.reshape(o, (np.int(np.size(o)/3), 3))
x = [0, 1, 2, 3, 4, 5, 6, 7, 8, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26,
     27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50]

x = [50]
goldsilverpolimer = load("guess.npy")
goldsilverpolimer = goldsilverpolimer[x]
print(len(goldsilverpolimer))
o = o[x]
sim_results = {
    "EZ": {},
    "EY": {}
}
counter = 0
for k in [mp.Ez, mp.Ey]:
    orancount = 0
    for j in o:
        ORAN = j
        guess = goldsilverpolimer[orancount]
        orancount += 1
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
        block_thicknessy = 0.25 * 1
        block_thicknessx = 0.02
        spacing_thickness_orj = 0.50
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
                spacing_thickness_orj*(iterator/3)
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
                    sim_results["EZ"][f"Gold: {ORAN[0]*100}%, Silver: {ORAN[1]*100}%, Pdms: {ORAN[2]*100}%"] = {}
                    sim_results["EZ"][f"Gold: {ORAN[0]*100}%, Silver: {ORAN[1]*100}%, Pdms: {ORAN[2]*100}%"][f"Spacing_{round(spacing_thickness,2)}"] = {
                        "Transmission": list(after_block_flux_second_run),
                        "Reflected": list(before_block_flux_second_run),
                        "Incident": list(after_block_flux)
                    }
                else:
                    sim_results["EZ"][f"Gold: {ORAN[0]*100}%, Silver: {ORAN[1]*100}%, Pdms: {ORAN[2]*100}%"][f"Spacing_{round(spacing_thickness,2)}"] = {
                        "Transmission": list(after_block_flux_second_run),
                        "Reflected": list(before_block_flux_second_run),
                        "Incident": list(after_block_flux)
                    }
            else:
                if(iterator == 0):
                    sim_results["EY"][f"Gold: {ORAN[0]*100}%, Silver: {ORAN[1]*100}%, Pdms: {ORAN[2]*100}%"] = {}
                    sim_results["EY"][f"Gold: {ORAN[0]*100}%, Silver: {ORAN[1]*100}%, Pdms: {ORAN[2]*100}%"][f"Spacing_{round(spacing_thickness,2)}"] = {
                        "Transmission": list(after_block_flux_second_run),
                        "Reflected": list(before_block_flux_second_run),
                        "Incident": list(after_block_flux)
                    }
                else:
                    sim_results["EY"][f"Gold: {ORAN[0]*100}%, Silver: {ORAN[1]*100}%, Pdms: {ORAN[2]*100}%"][f"Spacing_{round(spacing_thickness,2)}"] = {
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
with open('silvergoldpolimertest25error.json', 'w') as f:
    json.dump(sim_results, f)
    pass
