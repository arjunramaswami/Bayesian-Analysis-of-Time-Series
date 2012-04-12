from __future__ import division
import matplotlib.pyplot as plt
from scipy.integrate import dblquad
from scipy.misc import comb
from decimal import *
import numpy as np
import math

getcontext().prec = 10

def multiplicity(phase, omega, bins, timelist):
    
    timeperiod = (2*math.pi)/omega
    print "Phase", phase
    events_bin,binedges = np.histogram(timelist,np.arange(phase,max(timelist),timeperiod/bins))
    folded = [sum(events_bin[i::bins]) for i in range(0,bins)]
    
    remaining_bin = list(np.arange(phase,0,-(timeperiod/bins)))
    remaining_bin.append(0)
    remaining_bin.reverse()    
    
    addrem,bin_add = np.histogram(timelist,remaining_bin)
    addrem = list(addrem[::-1]) + [0 for _ in range(bins - len(addrem))]       
    addrem.reverse()
   
    folded = [(x + y) for x, y in zip(folded,addrem)]
    
    total = len(timelist)
    N = math.factorial(total)
    den = 1
    for i in folded:
        den = den*math.factorial(i)
    
    multi = np.divide(N,den)   
    print "Omega ",Decimal(omega)
    return 1/(Decimal(omega)*Decimal(multi))
    
def oddsratio(timelist, wlo, whi, bins, mmax):                            
        
        v = mmax -1
        const = 1/(2 * math.pi * v * math.log(whi/wlo))
        
        num = len(timelist)        
        c1 = num+bins-1        
        combination = comb(c1,num,exact = True)        
              
        pos_arr = bins**num   #pow(m,N)
        
        inw = dblquad(multiplicity, wlo, whi, lambda x:0, lambda x: 2*math.pi, args=(bins,timelist))
        print inw, " \n", pos_arr," \n", const, " \n",combination
        result = (pos_arr*inw)/(const*combination)    
        
        return result    