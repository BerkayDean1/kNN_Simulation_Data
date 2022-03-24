#!//usr/bin/python
  
#############################################################################
#to run: call python getASET filename vectorcolNumber                       #
#############################################################################
#Description: this script reads a .raw datafile and determines whether or   #   
#             an ASET occured, and if so, the width and amp of the transient#
#                                                                           #
#Author: Daniel Loveless (daniel-loveless@utc.edu)                          #
#Last Update: 05/05/2015                                                    #
#############################################################################

import glob

#datfile = r"C:\Users\berka\OneDrive - University of Tennessee at Chattanooga\
#     Research\python\LM124_Sim_Data\Q9_data\LM124_sim_SET_1m.sorted"
datafiles = sorted(glob.glob('LM124_sim_SET1_*.sorted'))
vecnum = 2 # Column in files with voltage values
tcol=1     #column in vector corresponding to the timestamps (default is 1)

#################
#import the file#
#################

writeFile = open("mag_pw.txt", "a")
writeFile.write("Node, Deposited Q (mA), Transient Magnitude(V), Pulse Width(s)\n")
writeFile.close()

##### Loop through all data files 
for datfile in datafiles:
     print(datfile)
     IOflag=0

     try:
          infile=open(datfile,'r')
          line=infile.readlines()
          infile.close()
     except IOError as err:
          IOflag=1
          errno, strerror = err.args
          print("I/O error(%s): %s" % (errno, strerror))

     if IOflag==0:
          ####################
          #grab the waveforms#
          ####################

          vec=[]    #vector for output data points
          tvec=[]   #vector for time data points
          temp=0    #temp for vec
          ttemp=0   #temp for tvec
          #print vecnum
          #loop through the length of line (number of vectors in file)
          for i in range(len(line)):
               a=[] #vector to hold data from line
               a=line[i].split()

               #place appropriate data points in file in temps
               if vecnum==0:
                    temp=0
               else:
                    temp=float(a[int(vecnum)])
                    ttemp=float(a[int(tcol)])
               #append temp value to appropriate vectors
               if vecnum==0:
                    vec=0
               else:
                    vec.append(temp)
                    tvec.append(ttemp)
          #print vec
          ###########################################################################
          #find the rising edge of the transient (if exists) and timestamp          #
          ###########################################################################

          flag=0            #flag for det if the last value was above or below thresh
          rf=0              #variable describing current value
          count=0           #counter incrementing every time a rising edge occurs
          tchk=[]           #vector for timestamps of each rising edge (50% point)
          numpulses=0       #the number of pulses (rising edges)
          initVal=float(vec[0])    #the initial value of the datafile
          maxVal=max(vec)   #the maximum value in vector
          thresh=(maxVal-initVal)/2+initVal
          print ("Initial Value=\t" + str(initVal))
          print ("Threshold set to=\t" + str(thresh))
          flag=0
          for j in range(1,len(vec)):       #loop through the clock vector
                    rf=vec[j]               #assign the current value in vector
                    if flag==1:             #if the last value was above thresh
                         if rf<=thresh:     #if the current value is below thresh
                              count=count+1
                              tchk.append(tvec[j])
                              flag=0        #set flag back to 0
                    else:                   #if last value was below thresh
                         if rf>=thresh:     #if the current value is above thresh
                              count=count+1 #then incremnent the counter
                              tchk.append(tvec[j]) #and record the timestamp
                              flag=1        #flag=1 when the threshold is exceeded
          numpulses=(count-1)               #the number of pulses
          print ("Total number of transients:\t" + str(numpulses) )
          print ("The voltage transients are:\t" + str(maxVal-initVal))
          ###########################################################################
          #                       find the transient width                          #
          ###########################################################################

          tdiff=0 #vector for the time differences between current and previous
          diff=0   #variable for time difference for current

          for k in range(1,count):    #loop through the timestamp vector
               diff=tchk[k]-tchk[k-1] #the time difference between pulses
               tdiff = diff    #append the current value to a new vector

          print ("The transient width(s) are:\t" + str(tdiff))

          ##########################################
          ## Writing to .txt file                 ##
          #############################################
          writeFile = open("mag_pw.txt", "a")
          writeFile.write('')
          writeFile.write(str(maxVal-initVal))
          writeFile.write(", ")
          writeFile.write(str(tdiff))
          writeFile.write("\n")
          writeFile.close()

          ##########################################
          ## Writing to CSV not working correctly ##
          #############################################
          # filename = "mag_pw.csv"
          # fields = ['Pulse Width (s)', 'Transient Magnitude (V)']
          # rows = [str(tdiff), str(maxVal-initVal)]
          # with open(filename, 'w') as csvfile:
          #      # creating a csv writer object 
          #      csvwriter = csv.writer(csvfile) 
          
          #      # writing the fields 
          #      csvwriter.writerow(fields) 
          
          #      # writing the data rows 
          #      csvwriter.writerows(rows)


