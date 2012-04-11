from __future__ import division
from decimal import *
import numpy as np
import matplotlib.pyplot as plt
import math
import BayesianInference as bi

"""
    facthist : Final time series (cps) after masking Eg: 9,25,31,-,-,9,9...
    number : Extend a single period to many Eg: 10
    timestamp : Collection of time stamp values  Eg: 1.23th sec, 2.5th sec
    leastcount : of machine Eg:0.1
    edge = bins : Array of successive least count values Eg: 0.1,0.2,0.3...
    normalhist : normalized time series cps before masking Eg: 9,25,31,25,9,9

    freq : 1/total period
    period : 1 wave (cycle)
    phase :
    amp :
    
    interval : 1-0/100
    
"""
class Wave:
    """ Super class Wave """
        
    def __init__(self,freq=None,phase=None,amp=None,period=None,cps=None):
        """ Initialize the parameters of the time series """
        self.freq = freq
        self.phase = phase
        self.amp = amp
        self.period = period
        self.cps = cps        
                
    def extend_profile(self,number=1):
        """ timestamp contains the whole time series over many periods """
        
        self.number=number
        temp=[x+y for x in np.arange(self.period/2,self.number*self.period,self.period/2) for y in self.timestamp]   
        self.timestamp=self.timestamp+temp
        
        #plt.plot(range(1,len(self.timestamp)+1),self.timestamp)
        #plt.show()

    def ts_generate(self,leastcount):
        """ Convert the time stamp data into photon arrival cps by binning with instrument least count"""
        """ id is Instrument Detections Eg:0.1"""
        
        self.leastcount = leastcount
        if self.leastcount>self.cps:
            print " Instrument Saturation \n Please enter lesser leastcount"
            
        else:
            self.bins = np.arange(0, max(self.timestamp)+self.leastcount, self.leastcount)   
            self.hist,self.id = np.histogram(self.timestamp,bins=self.bins)           
            
            d = dict(zip(self.id,self.hist))
            self.onlyone = [key for key,value in d.iteritems() if value==1.0]
            self.onlyone = sorted(self.onlyone)
            #print onlyone
            #plt.plot(self.id[1::],self.hist,'*')
            #plt.show()
        
    def masking(self,limit):
        s = map(lambda x:x*x,list(np.random.normal(0,1,math.ceil((self.period*self.number)/self.leastcount))))   #Creating random Gaussian values
        s = map(lambda x: x>limit and 1 or 0, s)            # Checking for threshold      
        self.maskedhist = np.ma.masked_where(s, self.normalhist)  # Masking time stamp data values based on the Gaussian missing values
        self.edge = self.edge[1::]                          # Excuding 0th value
        self.facthist = np.ma.masked_where(s,self.hist)     
        self.facthist = np.ma.filled(self.facthist,0)       #Contains final masked photon arrival cps 

        """ To consider instrumental errors, Gaussian masking is used in which randomized Gaussian values are masked checking a treshold """
        

class Sinwave(Wave):
    """ Creating sinwave for 1 period """   

    
    def __init__(self,freq = None,phase = None,amp = None,period = None,cps = None,interval=20):
        """ cps is the time of emission of photons from the source """
        """ timestamp is the collection of time stamps of detection of photons"""
        
        Wave.__init__(self,freq, phase, amp, period, cps)       
        self.interval = interval
        
        if self.freq is not None:
            omega = 2*math.pi * self.freq
        else:
            omega = (2*math.pi)/self.period
        
        self.timestamp = [( math.asin((math.sqrt(i/self.interval))/self.amp)-self.phase)/omega for i in range(1,self.interval+1)]
        
        maxtime=self.timestamp[-1]
        secondhalf =  map(lambda x: maxtime+(maxtime-x), self.timestamp[-1::-1])       
        self.timestamp=self.timestamp+secondhalf[1:]
              



