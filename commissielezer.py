import os

import numpy as np
from configuratie import rekeningenfile

def commissielijst():
    c_lijst = np.genfromtxt(os.path.dirname(os.path.realpath(__file__)) + "/rekeningen.csv", dtype = None, skip_header = 1, delimiter = ";")
    
    commissiedict = {}
    #Rekeningnummer index 1, commissie index 12
    for item in c_lijst:
        commissiedict[item[1]] = item[12]
        
    return commissiedict
        

def turflijst():
    c_lijst = commissielijst()
    lijst = set(c_lijst[item] for item in c_lijst if c_lijst[item]!= '')
    turfdict = {}
    for item in lijst:
        turfdict[item] = 0
    return turfdict