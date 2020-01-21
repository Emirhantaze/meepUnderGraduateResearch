import meep as mp
import numpy as np
import matplotlib.pyplot as plt
import math
s=1
cell_size = mp.Vector3(s*2,5*s,0)
pml_layers = [mp.PML(s/2)]
resolution = 25
minwvl=0.4
maxwvl=0.8
nwvl=10
wvlwidth=(maxwvl-minwvl)/(nwvl-1)
for wvl in np.arange(minwvl,maxwvl+wvlwidth,wvlwidth):
    sources = [mp.Source(mp.ContinuousSource(frequency=(1/wvl)),
                        component=mp.Ez,
                        center=mp.Vector3(-2*s,0),
                        size=mp.Vector3(0,1*s))]
        
    