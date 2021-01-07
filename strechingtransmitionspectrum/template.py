"""
this template file is designed for applying applications and saving vector-pictures of current python file
copy past relevant parts of this file to your original project to work 
"""
from datetime import datetime
import matplotlib.pyplot as plt
import meep as mp
import numpy as np
# from meep.materials import Au
goldsilverpolimer = np.load("guess.npy")
goldsilverpolimer = goldsilverpolimer[50]
guess = goldsilverpolimer
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


k = mp.Ey  # k is polarization component of source
offsetx = 0.05
block_thicknessy = 0.5 * 1
block_thicknessx = 0.02
spacing_thickness = block_thicknessy
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
symmetries = [mp.Mirror(mp.Y, phase=-1)]

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

sim.run(until_after_sources=mp.stop_when_fields_decayed(50, k, pt, 1e-3))


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
sim.run(until_after_sources=mp.stop_when_fields_decayed(50, k, pt, 1e-3))
after_block_flux_second_run = mp.get_fluxes(after_block)
before_block_flux_second_run = mp.get_fluxes(before_block)
# np.savetxt(f"tra_ez_ST{round(spacing_thickness,2)}.txt",after_block_flux_second_run)
# np.savetxt(f"ref_ez_ST{round(spacing_thickness,2)}.txt",before_block_flux_second_run)
# np.savetxt(f"in_ez_ST{round(spacing_thickness,2)}.txt",after_block_flux)
transmittance_ratio = np.divide(after_block_flux_second_run, after_block_flux)
wvls = np.divide(1, np.asarray(flux_freqs))
plt.plot(wvls, transmittance_ratio)
plt.title(
    f"resolution: {resolution}, dpml: {dpml}, blockspacing: {spacing_thickness}")
plt.xlabel("wavelengths")
plt.ylabel("transmission")
time = datetime.now().strftime("%d-%m-%Y_%I-%M-%S_%p")
name = __file__.split("/")
name = name[len(name)-1]
plt.show()
fig = plt.figure(1)
sim.plot2D()
plt.show()
#  plt.savefig(fname=f"/home/emirhan/meepUnderGraduateResearch/pictures/{name}-{time}.svg",format="svg")
