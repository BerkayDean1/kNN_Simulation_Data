import pandas as pd
from math import log

data = [[1, 2], [2, 5], [3, 4], [4,2], [5, 1]]
df_exp = pd.DataFrame(data, columns=['time', 'vout'])
vout_col = df_exp['vout']

## Max value of vout
peak = vout_col.max()
print(peak)

## Time at max value
t_peak = df_exp.loc[df_exp['vout'] == peak, 'time'].iloc[0]

## get fwhm function 
half_max = peak/2

## finding half max value
index = df_exp.index[df_exp['vout'] == peak].tolist()
df_exp_2 = df_exp[index[0]:len(df_exp)]
t_half_max = df_exp_2.loc[df_exp_2['vout'] < half_max, 'time'].iloc
print(t_half_max)
t_half_max = df_exp_2.loc[df_exp_2['vout'] < half_max, 'time'].iloc[0]
print(t_half_max)
## decay constant calculation for half-life
t_diff = t_peak - t_half_max
tau = (-1*log(2))/t_diff