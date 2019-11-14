from __future__ import division
import meep as mp
import matplotlib.pyplot as plt
import numpy as np
import math

print(math.pow(6.9,(1/2)))
Au = mp.Medium(index=math.pow(6.9,(1/2)))
dpml=1
sx=7
cell = mp.Vector3(7,3)
pml= mp.PML(1)
minwavelength=400
maxwavelength=800
minf=1/maxwavelength
maxf=1/minwavelength
fcen = (maxf+minf)/2  
df = maxf-minf
sources = [mp.Source(mp.GaussianSource(fcen,fwidth=df),
                     component=mp.Ez,
                     center=mp.Vector3(-2.5,0,0),
                     size=mp.Vector3(0,0.5,0))]

resulation = 20
for r in (np.arange(20,101,20))/1000:
    lightside_fr = mp.FluxRegion(center=mp.Vector3(-0.5*sx+dpml+0.5,wvg_ycen,0), 
                             size=mp.Vector3(0,1,0))
    