import matplotlib.pyplot as plt
import meep as mp
import numpy as np

from datetime import datetime
"""
defining au 
"""
x  = [1.78289910e+00, 1.00000000e-10, 1.34729698e+01, 7.20369796e+00,
       1.42305295e-07, 5.73419200e-01, 9.53801633e-01, 1.64525252e+00,
       1.05086993e+00, 2.26832125e-01, 2.75847736e+00, 3.64135525e-01,
       9.40636909e-01, 3.07875936e+00, 5.89122140e-01, 4.27335633e+00,
       3.83059318e+00, 1.95411014e-01, 1.55790666e+00]
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
difference = 0.1
setdiferrence = .1
iscontinue = True
iterator= 1 
lastitereation=5
while iscontinue:
    wvl_min = 0.400
    wvl_max = 0.700
    frq_min = 1/wvl_max
    frq_max = 1/wvl_min
    frq_cen = 0.5*(frq_min+frq_max)
    dfrq = frq_max-frq_min
    nfrq = 100
    Material= Au
    resolution = 500
    dpml = 0.11
    pml_layers = [mp.PML(dpml, direction=mp.X, side=mp.High),
                        mp.Absorber(dpml, direction=mp.X, side=mp.Low)]
    symmetries = [mp.Mirror(mp.X)]
    offsetx = 0.05
    block_thicknessy = 0.5 * 1
    block_thicknessx = 0.02
    spacing_thickness = block_thicknessy*setdiferrence#

    celly = (spacing_thickness+block_thicknessy)
    cellx = block_thicknessx+2*dpml+2*offsetx

    geometry=[]

    sources = [mp.Source(mp.GaussianSource(frq_cen,fwidth=dfrq,is_integrated=True),
                        center=mp.Vector3(-0.5*cellx+dpml+0.01),
                        size=mp.Vector3(0,celly),
                        component=mp.Hz)]
    sim = mp.Simulation(resolution=resolution,
                        # symmetries=symmetries,
                        cell_size=mp.Vector3(cellx,celly),
                        dimensions=3,
                        boundary_layers=pml_layers,
                        sources=sources,
                        ensure_periodicity=True,
                        k_point=mp.Vector3())

    transmittance_first_fr = mp.FluxRegion(center=mp.Vector3(0.5*cellx-dpml-0.01,0,0),size=mp.Vector3(0,celly))
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
                        # symmetries=symmetries,
                        cell_size=mp.Vector3(cellx,celly),
                        boundary_layers=pml_layers,
                        sources=sources,
                        k_point=mp.Vector3(),
                        ensure_periodicity=True,
                        geometry=geometry,
                        )

    transmittance_first = sim.add_flux(frq_cen,dfrq,nfrq,transmittance_first_fr)
    sim.run(until_after_sources=100)
    transmittance_second_flux =  mp.get_fluxes(transmittance_first)
    transmittance_ratio=np.divide(np.asarray(transmittance_second_flux),np.asarray(transmittance_first_flux))
    # transmittance_ratio = np.asarray(transmittance_second_flux)
    # transmittance_ratio=transmittance_ratio-np.mean(transmittance_ratio)
    wvls=np.multiply(np.divide(1,np.asarray(flux_freqs)),1000)
    # plt.figure(2)
    # sim.plot2D()
    # plt.show()
    plt.figure(1)
    np.savetxt(f"TREz_{iterator}.txt",transmittance_ratio)
    
    plt.plot(wvls,transmittance_ratio,color=f"C{iterator}",label=f"ST:{round(spacing_thickness,2)} BTY:{round(block_thicknessy,2)} ")
    setdiferrence+=difference
    sim.reset_meep()
    if(iterator==lastitereation):
        iscontinue=False
    else:
        iterator+=1
plt.title(f"TransmissionToWavelengths Resolution:{resolution} BTX:{round(block_thicknessx,2)} Polarization: Ez")
plt.xlabel("Wavelengths")
plt.ylabel("Transmission")

time = datetime.now().strftime("%d-%m-%Y_%I-%M-%S_%p")
name = __file__.split("/")
name=name[len(name)-1]
plt.legend()
plt.savefig(fname=f"/home/emirhantaze/github/meepUnderGraduateResearch/pictures/{name}_resolution_{resolution}_{time}.svg",format="svg")
# plt.show()