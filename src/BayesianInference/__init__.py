from __future__ import division
import matplotlib.pyplot as plt
from scipy.integrate import romberg
from scipy.misc import comb
from decimal import *
from numpy import histogram
from numpy import arange
import math

#getcontext().prec = 500

def multiplicity(phase, omega, bins, timelist):
    
    timeperiod = (2*math.pi)/omega
    
    events_bin,binedges = histogram(timelist,arange(phase,max(timelist),timeperiod/bins))
    folded = [sum(events_bin[i::bins]) for i in range(0,bins)]
    
    remaining_bin = list(arange(phase,0,-(timeperiod/bins)))
    remaining_bin.append(0)
    remaining_bin.reverse()    
    
    addrem,bin_add = histogram(timelist,remaining_bin)
    addrem = list(addrem[::-1]) + [0 for _ in range(bins - len(addrem))]    
    addrem.reverse()           
    folded = map(sum,folded,addrem)
    
    total = len(timelist)
    N = math.factorial(total)
    den = 1
    for i in folded:
        den = den*math.factorial(i)
    multi = N/den
   
    return multi

def phaseintegration(omega,bins,timelist):
    temp = romberg(multiplicity,0,2*math.pi,args=(omega,bins,timelist))
    return temp /omega
    
def oddsratio(timelist, wlo, whi, bins, mmax):                            
        
        v = mmax-1
        const = 1/(2 * math.pi * v * math.log(whi/wlo))
        
        num = len(timelist)        
        c1 = num+bins-1        
        combination = comb(c1,num,check = True)        
              
        pos_arr = bins**num   #pow(m,N)
        
        inw = romberg(phaseintegration, wlo, whi,args=(bins,timelist))
        
        result = (pos_arr*inw)/(const*combination)    
        
        return result    