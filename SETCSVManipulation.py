import time
fullTimeStart = time.time()
import os
#import threading 
import pandas as pan
import copy
import math 
import numpy 
#import tkinter
from matplotlib import pyplot as plt
class CSVReadandPlot():
    def __init__(self, fileName, loadNewFile = False, intervalSize = 0):
        startTime = time.time()
        self.fileName = fileName[0:len(fileName)-4]+"_stored.pkl" #the .pkl file where the file worked with is stored
        self.csvFileDF = pan.DataFrame.empty
        self.changedDF = False #used to see if the .pkf file stored needs to be updated or added
        #sees if the store file exists and if the user wants to load the file from storage or not
        if os.path.exists(self.fileName) and not loadNewFile:
            self.csvFileDF = pan.read_pickle(self.fileName)
        else: 
            self.csvFileDF = pan.read_csv(fileName)
            self.changedDF = True
        pan.set_option("display.max.columns", None)
        self.interval = 0
        titles = list(self.csvFileDF.columns)
        #will find the interval rate automatically. When it doesn't work, it'll ask you for it. 
        if intervalSize == 0:
            for i in range(0, len(titles)): #to auto find the interval
                if titles[i] == "Record Length":
                    try:
                        self.interval = int(titles[i+1])
                    except:
                        print("Cannot get the interval rate. What is it?")
                        self.interval = int(input())
                    break
            if self.interval == 0:
                print("Cannot get the interval rate. What is it?")
                self.interval = int(input())
        else:
            self.interval = intervalSize
        self.numInter = int(self.csvFileDF.iloc[:,0].size/self.interval)
        print("time to load csv", (time.time()-startTime)*1000, "milliseconds")
    def plotDataInter(self, DFColTitles, inter, showPlot = True, labelNames = None, fastPlot = False):
        #will allow for the plotting of data, put only the specified interval
        #DFColTitles involves what titles are being handled. It's a list. It goes [x, y]
        #labelNames is arranged like [xlabel, ylabel, title]
        csvData, = plt.plot(self.csvFileDF.loc[(inter*self.interval):(inter*self.interval+self.interval-1), DFColTitles[0]], self.csvFileDF.loc[(inter*self.interval):(inter*self.interval+self.interval-1), DFColTitles[1]], label = str(inter))
        if fastPlot:
            plt.style.use('fast')
        if labelNames:
            plt.xlabel(labelNames[0])
            plt.ylabel(labelNames[1])
            plt.title(labelNames[2])
        if showPlot:
            plt.show()
        return csvData
    def plotDataFull(self, DFColTitles, showPlot = True, labelNames = None, fastPlot = False):
        #will allow for the plotting of data in all of the intervals at once
        #DFColTitles involves what titles are being handled. It's a list. It goes [x, y]
        #labelNames is arranged like [xlabel, ylabel, title, addLegend?]
        csvPlot = plt.plot(self.csvFileDF.loc[:, DFColTitles[0]], self.csvFileDF.loc[:, DFColTitles[1]])
        if fastPlot:
            plt.style.use('fast')
        if labelNames:
            plt.xlabel(labelNames[0])
            plt.ylabel(labelNames[1])
            plt.title(labelNames[2])
            if labelNames[3]:
                plt.legend()
        if showPlot:
            plt.show()
    def clearPlot(self):
       plt.cla()
    def isChanged(self):
        return self.changedDF
    def saveWork(self):
        #save the work done to the .pkf file
        startTime = time.time()
        if self.changedDF:
            self.csvFileDF.to_pickle(self.fileName)
        print("time to save", (time.time()-startTime)*1000, "milliseconds")
    def pullFullDF(self):
        #the full DataFrame
        return self.csvFileDF
    def colTitles(self):
        #returns the titles of the pandas columns
        return list(self.csvFileDF.columns)
    def numIntervals(self):
        #returns the number of intervals in the test 
        return self.numInter
    def pullInterval(self, intervalIndex):
        #will pull the rows a part of a specified interval value
        #the intervalIndex starts at 0 and ends at the number of intervals-1. 
        #For instance intervalIndex = 0 will give you the first interval of data. 
        return self.csvFileDF.loc[(intervalIndex*self.interval):(intervalIndex*self.interval+self.interval-1), :]
    def pullCol(self, colToPull):
        #allows you to pull a specific column
        return self.csvFileDF.loc[:, colToPull]
    def pullCols(self, colsToPull):
        #allows you to pull specific columns
        #for this function, you place in all of the columns to pull
        return self.csvFileDF.loc[:, colsToPull]
    def pullRow(self, rowToPull):
        #allows you to pull a specific row 
        try:
            return self.csvFileDF.loc[rowToPull]
        except:
            print("TYPEError: You need to use an integer")
    def addInterval(self, desiredInterval, colTitle, dataToAdd):#untested
        #dataToAdd is a list/tuple
        lengthCol = self.csvFileDF.iloc[:,0].size
        while len(dataToAdd) < self.interval:
            dataToAdd.append(0)
        #print(len(self.csvFileDF.loc[(self.interval*desiredInterval)//lengthCol:((self.interval*desiredInterval)//lengthCol+self.interval), 'Time']))
        #print(len(dataToAdd[0:(len(dataToAdd))]))
        self.csvFileDF.loc[(self.interval*desiredInterval)//lengthCol:((self.interval*desiredInterval)//lengthCol+self.interval-1), colTitle] = dataToAdd[0:(len(dataToAdd))]
    def addCol(self, coltoAdd, colTitle, save = True): #will autosave work, unless directed.
        #add a column
        self.csvFileDF.loc[:, colTitle] = coltoAdd
        if save:
            self.saveWork()
    def addRow(self, rowtoAdd, rowTitle, save = True): #will autosave work, unless directed.
        #add a row
        self.csvFileDF.loc[rowTitle, :] = rowtoAdd
        if save:
            self.saveWork()
class manipulateSETData(CSVReadandPlot):
    def __init__ (self, fileName, loadNewFile=False, intervalSize = 0):
        super().__init__(fileName, loadNewFile, intervalSize)
    #all the other functions from CSVReadandPlot are in here. 
    def derivativeAll(self, colDy, colToModDx, derColName, windowSize = 1):
        startTime = time.time()
        #finds the derivative of the inputted SET based on the windowSize given. 
        storeNewCol = self.csvFileDF[colToModDx].copy()
        lengthCol = storeNewCol.size
        if windowSize >=self.interval: #error protection 
            print("Your interval is too big")
            self.csvFileDF.loc[:, derColName] = storeNewCol
            return
        #goes through everything and calculates the derivative based on each interval
        #timing: O(N) with no threading. unoptimized
        for i in range(0, lengthCol, self.interval):
            for j in range(i, i+self.interval-windowSize):
                if j % windowSize == 0:
                   #will only calculate the current derivative if the denominator is non-zero. If it is 0, then all discontinuities are just made equal to 0
                    if (self.csvFileDF.loc[j+windowSize, colDy]-self.csvFileDF.loc[j, colDy]) == 0:
                        storeNewCol[j] = 0
                    else:
                        storeNewCol[j] = (storeNewCol[j+windowSize]-storeNewCol[j])/(self.csvFileDF.loc[j+windowSize, colDy]-self.csvFileDF.loc[j, colDy])
                else:
                    #all values outside of the window size will become 0. 
                    storeNewCol[j] = 0
            storeNewCol[i+self.interval-windowSize: i+self.interval] = 0 #loads all the end values as 0, just because. 
        self.csvFileDF.loc[:, derColName] = storeNewCol
        self.changedDF = True
        print("End derivative calc", (time.time()-startTime)*1000, "milliseconds")
    def sumDataAll(self, colx, colToMody, sumBounds = None):   
        startTime = time.time()
        #integralBounds is based off of the minimum and maximum coly value desired. [mincoly, maxcoly] #this is next steps
        #returns the integral of each interval returned as a list
        #preliminary: slow. Technically O(N) because only touches each piece of all the data once
        integrals = [0.0]*self.numInter
        lengthCol = self.csvFileDF.loc[:,colToMody].size
        if not sumBounds:
            for i in range(0, lengthCol, self.interval):
                for j in range(i, i+self.interval):
                    integrals[i//self.interval] += self.csvFileDF.loc[j, colToMody] 
        else:
            for i in range(0, lengthCol, self.interval):
                activateMinBound = False
                deactivateMaxBound = False
                for j in range(i, i+self.interval-1):
                    if self.csvFileDF.loc[j, colx] == sumBounds[0]: #checks to see if min bound exists 
                            activateMinBound = True 
                    if self.csvFileDF.loc[j, colx] == sumBounds[1]: #checks to see if min bound exists 
                        deactivateMaxBound = True
                    if activateMinBound and not deactivateMaxBound: 
                        integrals[i//self.interval] += self.csvFileDF.loc[j, colToMody]
        print("End calculate sum all", (time.time()-startTime)*1000, "milliseconds")
        return integrals       
    def integralAllSquare(self, colx, colToMody, integralBounds = None):   
        startTime = time.time()
        #calculates the integral using squares. 
        #integralBounds is based off of the minimum and maximum colToMody value desired. [mincoly, maxcoly] #this is next steps
        #returns the integral of each interval returned as a list
        #preliminary: slow. Technically O(N) because only touches each piece of all the data once
        integrals = [0.0]*self.numInter
        lengthCol = self.csvFileDF.loc[:,colToMody].size
        if not integralBounds:
            for i in range(0, lengthCol, self.interval):
                for j in range(i, i+self.interval-1):
                    integrals[i//self.interval] += self.csvFileDF.loc[j, colToMody]
        else:
            for i in range(0, lengthCol, self.interval):
                activateMinBound = False
                deactivateMaxBound = False
                for j in range(i, i+self.interval-1):
                    if self.csvFileDF.loc[j, colx] == sumBounds[0]: #checks to see if min bound exists 
                            activateMinBound = True 
                    if self.csvFileDF.loc[j, colx] == sumBounds[1]: #checks to see if min bound exists 
                        deactivateMaxBound = True
                    if activateMinBound and not deactivateMaxBound: 
                        integrals[i//self.interval] += self.csvFileDF.loc[j, colToMody]
        print("End calculate sum all", (time.time()-startTime)*1000, "milliseconds")
        return integrals       
    def integralAllSquare(self, colx, colToMody, integralBounds = None):   
        startTime = time.time()
        #calculates the integral using squares. 
        #integralBounds is based off of the minimum and maximum colToMody value desired. [mincoly, maxcoly] #this is next steps
        #returns the integral of each interval returned as a list
        #preliminary: slow. Technically O(N) because only touches each piece of all the data once
        integrals = [0.0]*self.numInter
        lengthCol = self.csvFileDF.loc[:,colToMody].size
        if not integralBounds:
            for i in range(0, lengthCol, self.interval):
                for j in range(i, i+self.interval-1):
                    integrals[i//self.interval] += self.csvFileDF.loc[j, colToMody]*(self.csvFileDF.loc[j+1, colx]-self.csvFileDF.loc[j, colx]) #calculates the area of each time stamp Goes on lowest side. 
        else:
            for i in range(0, lengthCol, self.interval):
                activateMinBound = False
                deactivateMaxBound = False
                for j in range(i, i+self.interval-1):
                    if self.csvFileDF.loc[j, colx] == integralBounds[0]: #checks to see if min bound exists 
                            activateMinBound = True 
                    if self.csvFileDF.loc[j, colx] == integralBounds[1]: #checks to see if min bound exists 
                        deactivateMaxBound = True
                    if activateMinBound and not deactivateMaxBound: 
                        integrals[i//self.interval] += self.csvFileDF.loc[j, colToMody]*(self.csvFileDF.loc[j+1, colx]-self.csvFileDF.loc[j, colx]) 
        print("End calculate integral all", (time.time()-startTime)*1000, "milliseconds")
        return integrals
    def maximum(self, colx, colToMody):
        #returns a list of all of the maximum values of an interval 
        maxima = []
        for i in range(0, self.numInter):
            maxima.append([-9999999999, 0])
        lengthCol = self.csvFileDF.loc[:,colToMody].size
        for i in range(0, lengthCol, self.interval):
                for j in range(i, i+self.interval):
                    if self.csvFileDF.loc[j, colToMody] > maxima[i//self.interval][0]:
                        maxima[i//self.interval][0] = self.csvFileDF.loc[j, colToMody] 
                        maxima[i//self.interval][1] = j
        return maxima
    def averageFilterInterval(self, colx, colToMody, newColTitle, num4Average, intervalNum):
        #is an average filter which only handles a specific interval 
        self.changedDF = True
        averageFilterPiece = [1/num4Average]*num4Average
        fullConvolution = numpy.convolve(averageFilterPiece, self.csvFileDF.loc[(intervalNum*self.interval):(intervalNum*self.interval+self.interval), colToMody].to_numpy()).tolist()
        self.csvFileDF.loc[(intervalNum*self.interval):(intervalNum*self.interval+self.interval-1), newColTitle] = fullConvolution[0:self.interval]
    def averageFilter(self, colx, colToMody, newColTitle, num4Average):
        #generates a new column which is an average filter 
        self.changedDF= True 
        startTime = time.time()
        for i in range(0, self.numInter):
            self.averageFilterInterval(colx, colToMody, newColTitle, num4Average, i)
        print('Time for ALL AVERAGE FILTER', (time.time()-startTime)*1000, "milliseconds")
    def gaussianFilterInterval(self, colx, colToMody, newColTitle, stdDev, kernelSize, intervalNum):
        self.changedDF = True
        #first, need to make the kernel (the )
        #useful websites:
        #https://brilliant.org/wiki/kernel/
        #https://followtutorials.com/2013/02/gaussian-filter-generation-using-cc.html
        #https://homepages.inf.ed.ac.uk/rbf/HIPR2/gsmooth.htm
        #https://fiveko.com/gaussian-blur-filter/
        pi = 3.14159265358979323
        sqrt2pi = math.sqrt(2*pi)
        gaussianFilter = [0]*kernelSize
        sum = 0
        #creates the filter
        for i in range(-kernelSize//2, kernelSize//2):
            gaussian = (1/(sqrt2pi*stdDev))*(math.exp(-(i**2)/(2*(stdDev**2))))
            gaussianFilter[i+kernelSize//2] = gaussian
            sum += gaussian
        #normalizes the filter
        for i in range(0, kernelSize):
            gaussianFilter[i] /= sum
        #convolutes the data desired with the filter. 
        fullConvolution = numpy.convolve(gaussianFilter, self.csvFileDF.loc[(intervalNum*self.interval):(intervalNum*self.interval+self.interval), colToMody].to_numpy()).tolist()
        self.csvFileDF.loc[(intervalNum*self.interval):(intervalNum*self.interval+self.interval-1), newColTitle] = fullConvolution[0:self.interval]
    def gaussianFilter(self, colx, colToMody, newColTitle, stdDev, kernelSize):
        startTime = time.time()
        for i in range(0, self.numInter):
            self.gaussianFilterInterval(colx, colToMody, newColTitle, stdDev, kernelSize, i)
        print("end time gaussian filter", (time.time()-startTime)*1000, "milliseconds")
    def fullWidthHalfMaxWidths(self, colx, colToMody):
        #will return a list of the fullWidthHalfMax widths of all of the intervals structured like this:
        #returns the row numbers which correlate to the widths of each plot
        #will not draw a completely straight line. However, it will find the data points closest to the real value and go from there
        halfMax = self.maximum(colx, colToMody)
        maximum = halfMax #for this code, it doesn't matter that maximum points to halfMax, as all that matters is the row location of the maxima
        lengthCol = self.csvFileDF.loc[:,colToMody].size
        widthLoc = []
        for i in range(0, self.numInter):
            widthLoc.append([-1, -1])
        for i in range(0, len(halfMax)): 
            halfMax[i][0] /= 2
        for i in range(0, lengthCol, self.interval):
                currHalfMaxVal = 99999999999
                hitMax = False
                for j in range(i, i+self.interval):
                    if j == maximum[i//self.interval][1]:
                        hitMax = True
                        currHalfMaxVal = 99999999999
                    #before the maximum 
                    if not hitMax:
                        if abs(self.csvFileDF.loc[j,colToMody] - halfMax[i//self.interval][0]) < currHalfMaxVal: #
                            currHalfMaxVal = abs(self.csvFileDF.loc[j,colToMody] - halfMax[i//self.interval][0])
                            widthLoc[i//self.interval][0] = j
                    #after the maximum
                    else:
                        if abs(self.csvFileDF.loc[j,colToMody] - halfMax[i//self.interval][0]) < currHalfMaxVal:
                            currHalfMaxVal = abs(self.csvFileDF.loc[j,colToMody] - halfMax[i//self.interval][0])
                            widthLoc[i//self.interval][1] = j
                            return widthLoc
    def fullWidthHalfMax(self, colx, colToMody):
        #will return a list of the fullWidthHalfMax of all of the intervals structured like this:
        #returns the width based off of row numbers
        #will not draw a completely straight line. However, it will find the data points closest to the real value and go from there
        halfMax = self.maximum(colx, colToMody)
        maximum = halfMax
        lengthCol = self.csvFileDF.loc[:,colToMody].size
        widthLoc = []
        for i in range(0, self.numInter):
            widthLoc.append([-1, -1])
        for i in range(0, len(halfMax)): 
            halfMax[i][0] /= 2
        for i in range(0, lengthCol, self.interval):
                currHalfMaxVal = 99999999999
                hitMax = False
                for j in range(i, i+self.interval):
                    if j == maximum[i//self.interval][1]:
                        hitMax = True
                        currHalfMaxVal = 99999999999
                    #if we're on the left side of the maximum 
                    if not hitMax:
                        if abs(self.csvFileDF.loc[j,colToMody] - halfMax[i//self.interval][0]) < currHalfMaxVal:
                            currHalfMaxVal = abs(self.csvFileDF.loc[j,colToMody] - halfMax[i//self.interval][0])
                            widthLoc[i//self.interval][0] = j
                    #if we're on the right side of the maximum
                    else:
                        if abs(self.csvFileDF.loc[j,colToMody] - halfMax[i//self.interval][0]) < currHalfMaxVal:
                            currHalfMaxVal = abs(self.csvFileDF.loc[j,colToMody] - halfMax[i//self.interval][0])
                            widthLoc[i//self.interval][1] = j
        widths = [0]*self.numInter
        for i in range(0, self.numInter):
            widths[i] = widthLoc[i][1]-widthLoc[i][0]
        return widths
    def riseTime10_90_widths(self, colx, colToMody):
        #this function finds the rise time, starting with finding the data point closest to 10% of the maximum, then the data point closest to 90%, and then subtracts
        #uses rows to start with, and then will also use the difference between the rows, and then multiply it by the difference between the second and first colx values 
        #has a specific sensitivity to finding each of the 
        maximum = self.maximum(colx, colToMody)
        ninetyPercent = copy.deepcopy(maximum)
        tenPercent = copy.deepcopy(maximum)
        lengthCol = self.csvFileDF.loc[:,colToMody].size
        tenPLoc = [-1]*self.numInter
        ninetyPLoc = [-1]*self.numInter
        for i in range(0, len(tenPercent)): 
            tenPercent[i][0] /= 10
            ninetyPercent[i][0] = ninetyPercent[i][0]*9/10
        for i in range(0, lengthCol, self.interval):
                currTenPVal = 99999999999
                currNinetyPVal = 99999999999
                for j in range(i, maximum[i//self.interval][1]): #this loop will go until you hit the maximum
                        #gets closer and closer to the data point at the 10%
                        if abs(self.csvFileDF.loc[j,colToMody] - tenPercent[i//self.interval][0]) < currTenPVal:
                            currTenPVal = abs(self.csvFileDF.loc[j,colToMody] - tenPercent[i//self.interval][0])
                            tenPLoc[i//self.interval] = j
                        #gets the data closest to the 90%
                        if abs(self.csvFileDF.loc[j,colToMody] - ninetyPercent[i//self.interval][0]) < currNinetyPVal:
                            currNinetyPVal = abs(self.csvFileDF.loc[j,colToMody] - ninetyPercent[i//self.interval][0])
                            ninetyPLoc[i//self.interval] = j
        tenAndNinetyLoc = []
        for i in range(0, len(tenPLoc)):
            tenAndNinetyLoc.append([tenPLoc[i], ninetyPLoc[i]])
        return tenAndNinetyLoc
    def riseTime10_90(self, colx, colToMody):
        #this function finds the rise time, starting with finding the data point closest to 10% of the maximum, then the data point closest to 90%, and then subtracts
        #uses rows to start with, and then will also use the difference between the rows, and then multiply it by the difference between the second and first colx values 
        #this current iteration requires that row 1 and row 2's difference denotes the colx difference across all intervals and points
        #because of floating point subtraction not being the most accurate, a lot of the data will have a lot of 0.9999999s
        startTime = time.time()
        maximum = self.maximum(colx, colToMody)
        ninetyPercent = copy.deepcopy(maximum)
        tenPercent = copy.deepcopy(maximum)
        lengthCol = self.csvFileDF.loc[:,colToMody].size
        tenPLoc = [-1]*self.numInter
        ninetyPLoc = [-1]*self.numInter
        for i in range(0, len(tenPercent)): 
            tenPercent[i][0] /= 10
            ninetyPercent[i][0] = ninetyPercent[i][0]*9/10
        for i in range(0, lengthCol, self.interval):
                currTenPVal = 99999999999
                currNinetyPVal = 99999999999
                for j in range(i, maximum[i//self.interval][1]): #this loop will go until you hit the maximum
                        #gets closer and closer to the data point at the 10%
                        if abs(self.csvFileDF.loc[j,colToMody] - tenPercent[i//self.interval][0]) < currTenPVal:
                            currTenPVal = abs(self.csvFileDF.loc[j,colToMody] - tenPercent[i//self.interval][0])
                            tenPLoc[i//self.interval] = j
                        #gets the data closest to the 90%
                        if abs(self.csvFileDF.loc[j,colToMody] - ninetyPercent[i//self.interval][0]) < currNinetyPVal:
                            currNinetyPVal = abs(self.csvFileDF.loc[j,colToMody] - ninetyPercent[i//self.interval][0])
                            ninetyPLoc[i//self.interval] = j
        timeDiff = (self.csvFileDF.loc[2,colx]-self.csvFileDF.loc[1,colx])
        #print('time diff', timeDiff)
        for i in range(0, len(tenPLoc)):
            tenPLoc[i] = (ninetyPLoc[i] - tenPLoc[i])*timeDiff
        print("rise time calc", (time.time()-startTime)*1000)
        return tenPLoc
    def outline(self, colToMod, outlineColName): 
        startTime = time.time()
        #will pull the interval number which has the biggest area. 
        #this is done through using 2 metrics:
        #1. finding the maximum value of all intervals, keeping track of which interval piece is biggest
        #2. counting up those max values and return the one interval with the most maximums   
        #will read through the storeNewCol Series and identify the biggest values.
        #in it's current phase, it does not handle when more than one interval has an outline. 
        lengthCol = self.csvFileDF.loc[:,colToMod].size
        #maxIndex = [-1]*self.interval
        maxIndexVal = [-9999999]*self.interval
        countMax = [0]*self.numInter
        for i in range(0, lengthCol, self.interval):
            for j in range(i, i+self.interval):
                if self.csvFileDF.loc[j, colToMod] > maxIndexVal[j % (self.interval)]:
                    maxIndexVal[j % (self.interval)] = self.csvFileDF.loc[j, colToMod]
                    #maxIndex[j % self.interval ] = (i)/self.interval
                    countMax[int(((i)/self.interval))] += 1
        maxCount = -1
        maxIndex = -1
        for i in range(0, len(countMax)):
            if countMax[i] > maxCount:
                maxCount = countMax[i]
                maxIndex = i
        print("End outline calc", (time.time()-startTime)*1000, "milliseconds")
        return maxIndex