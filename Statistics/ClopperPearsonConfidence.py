import numpy as np
from scipy.stats import beta

k = [845, 8875]
N = [895, 161199]
eff = [ float(x)/y for x,y in zip(k,N) ]
alpha = 0.05
significance = alpha/2
confidence = 1-alpha

for valk,valN,vale in zip(k,N,eff):
       beta_lo = beta(valk,valN-valk+1)
       beta_hi = beta(valk+1, valN-valk)
       quant_lo = beta_lo.ppf(significance)
       quant_hi = beta_hi.ppf(1-significance)
       print('Low: ', quant_lo)
       print('Eff: ', vale)
       print('High: ', quant_hi)
       print()

