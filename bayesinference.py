from __future__ import division
import matplotlib.pyplot as plt
from decimal import *
import numpy as np
import math

getcontext().prec = 500

def modelbinning(startbin,timeobject,mmax):
    
    def oddsratio(bins):
        d = dict(zip(timeobject.id,timeobject.hist))
        onlyone = [key for key,value in d.iteritems() if value==1.0]
        onlyone = sorted(onlyone)
        events_bin, bin_edges = np.histogram(onlyone, np.arange(0,max(timeobject.timestamp)+timeobject.period,timeobject.period/bins))
        folded = [sum(events_bin[i::bins]) for i in range(0,bins)]                                 
        
        total = sum(events_bin)
        N = math.factorial(total)
        
        den = 1
        for i in folded:
            den = den*math.factorial(i)
        multiplicity = np.divide(N,den)
        print ""
        print math.log10(multiplicity)
    
    
        c1 = total+bins-1
        c2 = total
        c3 = c1-c2
        
        combination = math.factorial(c1)/(math.factorial(c2)*math.factorial(c3))
        pos_arr = int(bins)**int(total)
        
        result = Decimal(pos_arr)/(Decimal(multiplicity)*Decimal(combination)*Decimal(mmax-1))
        return result
    
    oddscomp = [oddsratio(i) for i in range(startbin,mmax+1)]
    x = [ math.log10(i)for i in oddscomp]    
    
    plt.plot(range(startbin,mmax+1),x)
    plt.show()    
    
def multiplicity(omega,bins,timestamplist):
    timeperiod = (2*math.pi)/omega
    
    events_bin,binedges = np.histogram(timestamplist,np.arange(phase,max(timestamplist)+(timeperiod/bins),timeperiod/bins))
    folded = [sum(events_bin[i::bins]) for i in range(0,bins)]
    
    remaining_bin = list(xrange(phase,0,-(timeperiod/bins)))
    remaining_bin.reverse()
    
    addrem,bin_add = np.histogram(timestamplist,remaining_bin)
    addrem.reverse()
    addrem = addrem+list(np.zeros(bins-len(addrem)))
    addrem.reverse()
           
    folded = map(sum,folded[-1::-1],addrem[-1::-1])
    
def phase():
    return (integrate.romberg(multiplicity,0,2*math.pi,args=(omega,bins))/omega)

temp = integrate.romberg(phase,wlo,whi)
    
    
    
