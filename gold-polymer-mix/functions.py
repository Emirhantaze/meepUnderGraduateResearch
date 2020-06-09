import numpy as np 
def mixsolver(f,e,e1):
    return [(2/(1-f)),((e-e1)*((3*f-1)/(f-1))),((e*e1)/(f-1))]
def calcdrude(frequency,frequencyn, gamma, sigma):
    return -frequencyn*frequencyn / (frequency*(frequency + 1j*gamma)) * sigma

def calclorentizan(frequency,frequencyn, gamma, sigma):
    return frequencyn*frequencyn / (frequencyn*frequencyn - frequency*frequency - 1j*gamma*frequency) * sigma