import meep as mp
import numpy as np 

def calc(varibles,orginal,depth):

    um_scale = 1
    say = 0
    eV_um_scale = um_scale/1.23984193
    Au_plasma_frq = 9.03*eV_um_scale
    metal_range = mp.FreqRange(min=um_scale/6.1992, max=um_scale/.24797)
    out = []
    var = [np.linspace(varibles[j][0],varibles[j][1],5) for j in range(6)]
    correlation = -1
    Au_f0 = 0.760
    for i in range(5):
        Au_frq0 = var[0][i]
        Au_gam0 = 0.053*eV_um_scale
        Au_sig0 = Au_f0*Au_plasma_frq**2/Au_frq0**2
        Au_f1 = 0.024
        for j in range(5):
            Au_frq1 = var[1][j]*eV_um_scale      # 2.988 um
            Au_gam1 = 0.241*eV_um_scale
            Au_sig1 = Au_f1*Au_plasma_frq**2/Au_frq1**2
            Au_f2 = 0.010
            for k in range(5):
                Au_frq2 = var[2][k]*eV_um_scale      # 1.494 um
                Au_gam2 = 0.345*eV_um_scale
                Au_sig2 = Au_f2*Au_plasma_frq**2/Au_frq2**2
                Au_f3 = 0.071
                for l in range(5):
                    Au_frq3 = var[3][l]*eV_um_scale      # 0.418 um
                    Au_gam3 = 0.870*eV_um_scale
                    Au_sig3 = Au_f3*Au_plasma_frq**2/Au_frq3**2
                    Au_f4 = 0.601
                    for m in range(5):
                        Au_frq4 = var[4][m]*eV_um_scale      # 0.288 um
                        Au_gam4 = 2.494*eV_um_scale
                        Au_sig4 = Au_f4*Au_plasma_frq**2/Au_frq4**2
                        Au_f5 = 4.384
                        for n in range(5):
                            Au_frq5 = var[5][n]*eV_um_scale      # 0.093 um
                            Au_gam5 = 2.214*eV_um_scale
                            Au_sig5 = Au_f5*Au_plasma_frq**2/Au_frq5**2


                            Au_susc = [mp.DrudeSusceptibility(frequency=Au_frq0, gamma=Au_gam0, sigma=Au_sig0),
                                    mp.LorentzianSusceptibility(frequency=Au_frq1, gamma=Au_gam1, sigma=Au_sig1),
                                    mp.LorentzianSusceptibility(frequency=Au_frq2, gamma=Au_gam2, sigma=Au_sig2),
                                    mp.LorentzianSusceptibility(frequency=Au_frq3, gamma=Au_gam3, sigma=Au_sig3),
                                    mp.LorentzianSusceptibility(frequency=Au_frq4, gamma=Au_gam4, sigma=Au_sig4),
                                    mp.LorentzianSusceptibility(frequency=Au_frq5, gamma=Au_gam5, sigma=Au_sig5)]
                            Au = mp.Medium(epsilon=1.0, E_susceptibilities=Au_susc, valid_freq_range=metal_range)
                            freqs = np.linspace(um_scale/0.7,um_scale/0.35,101)
                            au = np.empty(101,dtype=np.cdouble)
                            say=say+1
                            for ii in range (101):
                                au[ii]= Au.epsilon(freqs[ii])[1][1]  
                            temp = np.corrcoef(au,orginal)[0][1]
                            if(correlation<temp):
                                correlation = temp
                                print(correlation)
                                out = [i,j,k,l,m,n]
                                print(out)