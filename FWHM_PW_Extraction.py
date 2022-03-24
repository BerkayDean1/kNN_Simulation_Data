# Author: Kendra Davidson
# Last updated: 4/22/21
# Description:
# This program imports SET data from a csv file. A heatmap of the voltage and time 
# of every SET is generated. The data is put through a gaussian filter and a 
# heatmap of the full width half max and rise time is generated. A scatter plot
# of the full width half max and rise time is also generated. 
# The SETCSVManipulation.py file is used for several functions throughout this 
# program. 
###############################################################################################
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

#import SET manipulation class
# import sys
# sys.path.append(r'C:\Users\kendr\SETCSVManipulation.py')

#from SETCSVManipulation import manipulateSETData as scm
#from SETCSVManipulation import CSVReadandPlot as scm
from SETCSVManipulation import manipulateSETData as scm

# function to round numbers in scientific notation
def precision_round(number, digits):
    power = "{:e}".format(number).split('e')[1]
    return round(number, -(int(power) - digits))

#import CSVs
## Change these files to names of our csv
SET_test = pd.read_csv(r'C:\Users\kendr\SET_Detector_Test1_Ch1.csv')
SET_data = pd.read_csv(r'C:\Users\kendr\SET_Test_Data.csv')

#generate heatmap of voltage and time of all SETs
SET1 = SET_data.groupby(['Voltage','Time'])
SET_cnt = SET1.id.nunique()
SET1_cnt = SET_cnt.loc[:,:,:].reset_index().pivot(index='Voltage', columns='Time')
SET1_cnt.fillna(0, inplace=True)
hm = sns.heatmap(SET1_cnt)
plt.show()
#heatmap of full width half max and rise time of all SETs

#initialize SETCSVManipulation
#constant variables
intervalsize = 2500; #number of points per run
SETNum = 53; ## Change to number of simulations
test = scm('SETData.csv', loadNewFile = True, intervalSize = intervalsize)

#use gaussian filter on data
#Current is column being modified, new data put in Current2
test.gaussianFilter('Time', 'Current', 'Current2', stdDev=30, kernelSize=15)

#initialize array to store new data
SETArray = [[0 for i in range(3)] for j in range(SETNum)]

#calculate full width half max
SETCol = test.fullWidthHalfMax('Time', 'Current2') #interval is 2500, or # of points per run

#calculate rise time
SETRow = test.riseTime10_90('Time','Current2')

#insert data into new array
for r in range(SETNum):
    SETRow[r] = precision_round(SETRow[r],4)
    SETArray[r][0] = SETCol[r]
    SETArray[r][1] = SETRow[r]
    SETArray[r][2] = r
    
#save array
np.savetxt("test.csv", SETArray, delimiter=",",header="FWHM,RT,id")

#import array
SET_data2 = pd.read_csv(r'C:\Users\kendr\test.csv')

#modify data as needed for heatmap
SET_data2 = SET_data2.groupby(['# FWHM','RT'])
SET_cnt2 = SET_data2.id.nunique()
SET1_cnt2 = SET_cnt2.loc[:,:,:].reset_index().pivot(index='# FWHM', columns='RT')
SET1_cnt2.fillna(0, inplace=True)

#generate heatmap
hm2 = sns.heatmap(SET1_cnt2) #, xticklabels=SETRow)

#set axis titles
hm2.set(title="SET Heatmap",
       xlabel="Rise Time (s)",
      ylabel="Full Width Half Max (s)",)

#show heatmap
plt.show()

#generate scatter plot of full width half max and rise time
plt.scatter(SETCol, SETRow)
plt.title("SET Scatter Plot")
plt.xlabel("Rise Time (s)")
plt.ylabel("Full Width Half Max (s)")
plt.show()