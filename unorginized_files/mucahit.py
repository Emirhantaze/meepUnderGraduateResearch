import numpy as np
import meep as mp 
import matplotlib.pyplot as plt
dpml = 1
flag = True
while(flag):
        maxwvl = 0.750
        minwvl = 0.350
        frq_min = 1/maxwvl
        frq_max = 1/minwvl
        frq_cen = 0.5*(frq_min+frq_max)
        dfrq = frq_max-frq_min
        nfrq = 100  
        resolution = 110# this value will change 
        dpml = 2
        #wavelength resolution problem 
        #transmittance ratio is low 
        #silicon dioxide
        #titanium dio
        pml_layers = [mp.PML(dpml, direction=mp.Y, side=mp.High),
                        mp.Absorber(dpml, direction=mp.Y, side=mp.Low)]
        block_number = 6 # here this number determines how many dielectric material has been used
        Material = mp.Medium(epsilon=12)
        block_thicknessy = 0.1
        block_thicknessx = 0.1 #thickness of each block
        cellx = block_thicknessx 
        celly = 2 * dpml + block_number * 2 * (block_thicknessy)
        geometry = []

        sources = [mp.Source(mp.GaussianSource(frq_cen,fwidth=dfrq),
                        center=mp.Vector3(0,-0.5 * celly+dpml),
                        size=mp.Vector3(block_thicknessx,0),
                        component=mp.Ez)]  #polarization?
        sim = mp.Simulation(resolution=resolution,
                        cell_size=mp.Vector3(cellx,celly),
                        boundary_layers=pml_layers,
                        sources=sources,                
                        ensure_periodicity=True,
                        k_point=mp.Vector3())

        transmittance_first_fr = mp.FluxRegion(center = mp.Vector3(0,0.5 * celly - dpml,0),size = mp.Vector3(block_thicknessx))
        transmittance_first = sim.add_flux(frq_cen, dfrq, nfrq, transmittance_first_fr)
        pt = mp.Vector3(0, 0.5 * celly-dpml, 0)    # ?
        sim.run(until_after_sources=mp.stop_when_fields_decayed(50, mp.Ez,pt,1e-2))

        transmittance_first_flux =  mp.get_fluxes(transmittance_first)
        flux_freqs = mp.get_flux_freqs(transmittance_first)
        flux_freqs = mp.get_flux_freqs(transmittance_first)
        sim.reset_meep()

        SiO2 = mp.Medium(index=1.45)

        Ti = mp.Medium(index = 2.61)

        for i in range(block_number):
                geometry.append(mp.Block(mp.Vector3(block_thicknessx, block_thicknessy,mp.inf),
                                center=mp.Vector3(0,(block_thicknessy/2)+dpml-(celly/2)+2*i*block_thicknessy),
                                material=SiO2)) # it was equal to Materials
                                
                        #I added the geometry below but did not work
                geometry.append(mp.Block(mp.Vector3(block_thicknessx, block_thicknessy,mp.inf),
                                center=mp.Vector3(0,(block_thicknessy/2)+dpml-(celly/2)+(2*i+1)*block_thicknessy),
                                material=Ti)) 
        pt = mp.Vector3(0,celly*0.5-dpml)
        sim = mp.Simulation(resolution=resolution,
                        cell_size=mp.Vector3(cellx,celly),
                        boundary_layers=pml_layers,
                        sources=sources,
                        k_point=mp.Vector3(),
                        ensure_periodicity=True,
                        geometry=geometry)
        transmittance_first = sim.add_flux(frq_cen,dfrq,nfrq,transmittance_first_fr)
        sim.run(until_after_sources=mp.stop_when_fields_decayed(50,mp.Ez,pt,1e-2))
        transmittance_second_flux =  mp.get_fluxes(transmittance_first)

        transmittance_ratio=np.divide(np.asarray(transmittance_second_flux),np.asarray(transmittance_first_flux))
        wvls=np.divide(1,np.asarray(flux_freqs))
        plt.plot(wvls,transmittance_ratio)
        plt.xlabel("Wavelength")
        plt.ylabel("Reflection")
        plt.show()
        plt.plot(wvls,transmittance_ratio,color="r")
        a = input("enter True if not converged: ")
        if(a=="True"):
                flag=False
        
print("resolution: "+str(resolution))
