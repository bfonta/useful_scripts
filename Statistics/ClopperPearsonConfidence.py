import numpy as np
from scipy.stats import beta, binom

# k = [845, 8875]
# N = [895, 161199]
k = [845]
N = [895]
eff = [ float(x)/y for x,y in zip(k,N) ]
alpha = 0.05
significance = alpha/2
confidence = 1-alpha

# using definition with beta functions
for valk,valN,vale in zip(k,N,eff):
       beta_lo = beta(valk,valN-valk+1)
       beta_hi = beta(valk+1, valN-valk)
       quant_lo = beta_lo.ppf(significance)
       quant_hi = beta_hi.ppf(1-significance)
       print('Low: ', quant_lo)
       print('Eff: ', vale)
       print('High: ', quant_hi)
       print()

# using definition with binomials
for valk,valN,vale in zip(k,N,eff):
    p_right, p_left = 0, 0
    steps = 10001
    for p_iter in np.linspace(valk/valN,1.,steps):
        sum_left = 0
        fn = binom(valN, p_iter)
        for k_left in range(0,valk+1):
            sum_left += fn.pmf(k_left)
        #print(p_iter, sum_left, significance)
        if sum_left <= significance:
            p_left = p_iter
            break
        
    for p_iter in np.linspace(0,valk/valN,steps)[::-1]:
        sum_right = 0
        fn = binom(valN, p_iter)
        for k_right in range(valk,valN+1):
            sum_right += fn.pmf(k_right)
        # print(p_iter, sum_right, significance)
        if sum_right <= significance:
            p_right = p_iter
            break

    print('Low: ', p_right)
    print('Eff: ', vale)
    print('High: ', p_left)
    print()
    
