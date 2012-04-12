import timeseries as ts
import bayesinference as bi
sw = ts.Sinwave(phase=0,amp=1,period=3.24,cps=0.13)
sw.extend_profile(number=10)
sw.ts_generate(leastcount=0.017)
bi.modelbinning(2,sw)
