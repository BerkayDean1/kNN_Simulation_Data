import glob
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
filenames = sorted(glob.glob('LM124_sim_SET1_ASET_QR_*.sorted'))
print(filenames)
for filename in filenames:
    print(filename)
    D = np.loadtxt(fname=filename,dtype=np.float64)
    cols = ["val", "time", "vout", "vin"]
    df = pd.DataFrame(D,columns=cols)
    # df = df.set_index(df['time'])
    # df[['vout']].plot ()
    # plt.ylabel('Voltage (V)')
    # plt.xlabel('Time (s)')
    # plt.title(filename)
    # plt.show()