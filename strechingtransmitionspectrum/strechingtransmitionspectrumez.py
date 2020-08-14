import matplotlib.pyplot as plt
import meep as mp
import numpy as np

from datetime import datetime
"""
defining au 
"""
sim_results = {
    "EZ":{},
    "EY":{}
}
for k in [mp.Ez,mp.Ey]:
    for j in [0.4,0.5,0.6,0.7,0.8,0.9]:
        ORAN = j

        guess = []
        if(ORAN==0.4):

        # for 0.4 portion

            guess = [1.34838676e+00, 1.00000000e-10, 1.34647873e+01, 8.97296436e+00,
            6.32379608e-01, 7.43462500e-01, 1.00000000e-10, 1.00000000e-10,
            1.57588335e+00, 1.59673438e+00, 2.00000369e+00, 9.48842434e-01,
            6.72023538e-01, 2.89049334e+00, 5.06863406e-01, 3.78504277e+00,
            3.51143233e+00, 6.41451882e-01, 2.41680535e+00]

        elif(ORAN==0.5):

        # for 0.5 portion
        
            guess = [1.59494391e+00, 1.00000000e-10, 1.35059776e+01, 9.04275486e+00,
            2.03823256e-03, 5.57132001e-01, 5.11096419e+00, 3.07038611e+00,
            2.69917661e-01, 1.21603262e+00, 2.03617915e+00, 1.05613396e+00,
            2.53356956e-01, 2.75265033e+00, 3.47707931e-01, 1.10361139e+00,
            3.06365318e+00, 5.84536890e-01, 1.69056771e+00]


        elif(ORAN==0.6):
        # for 0.6 portion
        
            guess = [1.85363891e+00, 1.00000000e-10, 1.35059494e+01, 9.08226291e+00,
            3.88960804e-05, 1.00000000e-10, 2.61699241e+00, 2.99609943e+00,
            1.00000000e-10, 7.51361132e-01, 2.05864823e+00, 7.71673604e-01,
            1.39971789e-01, 2.72306612e+00, 3.56756627e-01, 3.09821906e+00,
            3.13065592e+00, 1.12911764e+00, 2.14526970e+00]

        elif(ORAN==0.7):

        # for 0.7 portion
        
            guess = [2.30198919e+00, 1.00000000e-10, 1.35055163e+01, 9.44034985e+00,
            1.15389461e-07, 1.00000000e-10, 1.00000000e-10, 2.11120653e+00,
            1.48482852e+00, 4.55102547e-02, 2.28683418e+00, 2.30763563e-01,
            8.69164922e-01, 2.77465072e+00, 6.98504333e-01, 1.75176559e+00,
            3.33262868e+00, 7.39833429e-01, 4.44926251e+00]

        elif(ORAN==0.8):

        # for 0.8 portion
        
            guess = [2.56585904e+00, 5.41312887e-01, 1.34722815e+01, 9.31369499e+00,
            8.24073644e-07, 2.36648954e-04, 1.00000000e-10, 2.02697068e+00,
            1.49947299e+00, 1.68415862e-01, 2.65663214e+00, 3.36348966e-01,
            5.68494883e-01, 2.91251561e+00, 5.77904604e-01, 2.28981861e+00,
            3.49458098e+00, 8.28291250e-01, 4.08091959e+00]

        elif(ORAN==0.9):

        # for 0.9 portion
        
            guess = [2.81964818e+00, 5.75966884e-01, 1.34712675e+01, 9.34091969e+00,
            2.13727362e-07, 1.00000000e-10, 1.00000000e-10, 2.01465360e+00,
            1.50491543e+00, 1.38084209e-01, 2.66097091e+00, 3.02715534e-01,
            5.02390308e-01, 2.90266673e+00, 5.49154469e-01, 2.36483816e+00,
            3.48757549e+00, 8.84746262e-01, 4.39823181e+00]


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
                mp.LorentzianSusceptibility(frequency=Au_frq1, gamma=Au_gam1, sigma=Au_sig1),
                mp.LorentzianSusceptibility(frequency=Au_frq2, gamma=Au_gam2, sigma=Au_sig2),
                mp.LorentzianSusceptibility(frequency=Au_frq3, gamma=Au_gam3, sigma=Au_sig3),
                mp.LorentzianSusceptibility(frequency=Au_frq4, gamma=Au_gam4, sigma=Au_sig4),
                mp.LorentzianSusceptibility(frequency=Au_frq5, gamma=Au_gam5, sigma=Au_sig5)]

        Au = mp.Medium(epsilon=x[18] , E_susceptibilities=Au_susc)

        """
        """
        # from meep.materials import Au
        offsetx = 0.05
        block_thicknessy = 0.5 * 1
        block_thicknessx = 0.02
        spacing_thickness_orj = block_thicknessy
        iscontinue = True
        iterator= 0
        lastitereation=3
        while iscontinue:
            spacing_thickness = spacing_thickness_orj + spacing_thickness_orj*(iterator/lastitereation)
            wvl_min = 0.400
            wvl_max = 0.700
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
            if (k == mp.Ey):
                symmetries = [mp.Mirror(mp.Y,phase=-1)]
            else:
                symmetries = [mp.Mirror(mp.Y)]

            celly = (spacing_thickness+block_thicknessy)
            cellx = block_thicknessx+2*dpml+2*offsetx

            geometry=[]

            sources = [mp.Source(mp.GaussianSource(frq_cen,fwidth=dfrq,is_integrated=True),
                                center=mp.Vector3(-0.5*cellx+dpml+0.01),
                                size=mp.Vector3(0,celly),
                                component=k)]
            sim = mp.Simulation(resolution=resolution,
                                symmetries=symmetries,
                                cell_size=mp.Vector3(cellx,celly),
                                dimensions=3,
                                boundary_layers=pml_layers,
                                sources=sources,
                                ensure_periodicity=True,
                                k_point=mp.Vector3())

            after_block_fr = mp.FluxRegion(center=mp.Vector3(0.5*cellx-dpml-0.01,0,0),size=mp.Vector3(0,celly))
            before_block_fr = mp.FluxRegion(center=mp.Vector3(-0.5*cellx+dpml+0.02,0,0),size=mp.Vector3(0,celly))

            after_block = sim.add_flux(frq_cen,dfrq,nfrq,after_block_fr)
            before_block = sim.add_flux(frq_cen,dfrq,nfrq,before_block_fr)
            pt = mp.Vector3(0.5*cellx-dpml-0.01,0,0)

            sim.run(until_after_sources=mp.stop_when_fields_decayed(50,k,pt,1e-3))


            after_block_flux =  mp.get_fluxes(after_block)
            before_block_flux_data = sim.get_flux_data(before_block)
            flux_freqs = mp.get_flux_freqs(after_block)

            sim.reset_meep()
            geometry=[mp.Block(mp.Vector3(block_thicknessx,block_thicknessy,mp.inf),
                                center=mp.Vector3(),
                                material=Material)]
            sim = mp.Simulation(resolution=resolution,
                                symmetries=symmetries,
                                cell_size=mp.Vector3(cellx,celly),
                                boundary_layers=pml_layers,
                                sources=sources,
                                k_point=mp.Vector3(),
                                ensure_periodicity=True,
                                geometry=geometry,
                                )
            before_block = sim.add_flux(frq_cen,dfrq,nfrq,before_block_fr)
            
            after_block = sim.add_flux(frq_cen,dfrq,nfrq,after_block_fr)
            sim.load_minus_flux_data(before_block,before_block_flux_data)
            sim.run(until_after_sources=mp.stop_when_fields_decayed(50,k,pt,1e-3))
            after_block_flux_second_run=  mp.get_fluxes(after_block)
            before_block_flux_second_run = mp.get_fluxes(before_block)
            # np.savetxt(f"tra_ez_ST{round(spacing_thickness,2)}.txt",after_block_flux_second_run)
            # np.savetxt(f"ref_ez_ST{round(spacing_thickness,2)}.txt",before_block_flux_second_run)
            # np.savetxt(f"in_ez_ST{round(spacing_thickness,2)}.txt",after_block_flux)
            if(k==mp.Ez):
                if(iterator==0):
                    sim_results["EZ"][f"Ratio_{ORAN}"] = {}
                    sim_results["EZ"][f"Ratio_{ORAN}"][f"Spacing_{round(spacing_thickness,2)}"]={
                        "Transmission":list(after_block_flux_second_run),
                        "Reflected":list(before_block_flux_second_run),
                        "Incident":list(after_block_flux)
                    }
                else:
                    sim_results["EZ"][f"Ratio_{ORAN}"][f"Spacing_{round(spacing_thickness,2)}"]={
                        "Transmission":list(after_block_flux_second_run),
                        "Reflected":list(before_block_flux_second_run),
                        "Incident":list(after_block_flux)
                    }
            else:
                if(iterator==0):
                    sim_results["EY"][f"Ratio_{ORAN}"] = {}
                    sim_results["EY"][f"Ratio_{ORAN}"][f"Spacing_{round(spacing_thickness,2)}"]={
                        "Transmission":list(after_block_flux_second_run),
                        "Reflected":list(before_block_flux_second_run),
                        "Incident":list(after_block_flux)
                    }
                else:
                    sim_results["EY"][f"Ratio_{ORAN}"][f"Spacing_{round(spacing_thickness,2)}"]={
                        "Transmission":list(after_block_flux_second_run),
                        "Reflected":list(before_block_flux_second_run),
                        "Incident":list(after_block_flux)
                    }
            sim.reset_meep()
            if(iterator==lastitereation):
                iscontinue=False
            else:
                iterator+=1
import json
sim_results["Other_Params"] = f"Resolution={resolution},BlockThicknessY={block_thicknessy},BlockThicknessX={block_thicknessx},PML={dpml},cellx={cellx},celly={celly}"
sim_results["Wavelengths"] = list(1/np.asarray(flux_freqs))
with open('results.json', 'w') as f:
    json.dump(sim_results, f)
    pass