from __future__ import division
import matplotlib.pyplot as plt
from scipy.integrate import romberg
from scipy.misc import comb
from decimal import *
import numpy as np
import math

getcontext().prec = 10

def multiplicity(phase, omega, bins, timelist,pos_arr):
    
    timeperiod = (2*math.pi)/omega
        
    events_bin,binedges = np.histogram(timelist,np.arange(phase,max(timelist),timeperiod/bins))
    folded = [sum(events_bin[i::bins]) for i in range(0,bins)]
    
    remaining_bin = list(np.arange(phase,0,-(timeperiod/bins)))
    remaining_bin
    remaining_bin.append(0)
    remaining_bin.reverse()    
    remaining_bin = [ i for i in remaining_bin if i >=0]      
    
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
    
    return (pos_arr/multi)

def phaseintegration(omega,bins,timelist,pos_arr):
    temp = romberg(multiplicity ,0 ,2*math.pi ,args = (omega,bins,timelist,pos_arr) ,divmax = 1)
    return (temp/omega)
    
def oddsratio(timelist, wlo, whi, bins, mmax):                            
        
        v = mmax - 1
        const = 1/(2 * math.pi * v * math.log(whi/wlo))

        num = len(timelist)
        
        result = []
        for i in range(bins,mmax):        
            c1 = num + i - 1        
            combination = comb(c1,num,exact = True)        
              
            pos_arr = i**num   
        
            inw = romberg(phaseintegration ,wlo ,whi ,args = (i,timelist,pos_arr), divmax = 1 )
            
            a = (inw)/(const*combination)
            result.append(a) 
       
        plt.plot(range(bins,mmax),result)
        plt.show()
        return result  
    
    
      
"""

def multiplicity(phase, omega, bins, timelist, pos_arr):
    
    timeperiod = (2*math.pi)/omega
    #print "Phase", phase
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
    temp = pos_arr/multi
    print " multi ", multi,"  ", pos_arr
    return (temp/omega)
    
def oddsratio(timelist, wlo, whi, bins, mmax):                            
        
        v = mmax -1
        const = 1/(2 * math.pi * v * math.log(whi/wlo))
        
        result = []
        
        num = len(timelist)
        for i in range(bins,mmax):         
            c1 = num + i - 1        
            combination = comb(c1,num,exact = True)      
                  
            pos_arr = i**num   #pow(m,N)
            
            inw = dblquad(multiplicity, wlo, whi, lambda x:0, lambda x: 2*math.pi, args=(i,timelist,pos_arr))
            print inw, " \n", pos_arr," \n", const, " \n",combination
            a = (inw)/(const*combination)    
            result.append(a) 
       
        plt.plot(range(bins,mmax),result)
        plt.show()
        return result  
"""       