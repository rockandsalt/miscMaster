

import pyDOE
import numpy as np
import pandas as pd

def createSeries(listOfIndex,listOfVal):
    newArray = []
    for index in listOfIndex:
        newArray.append(listOfVal[int(index)])

    return pd.Series(newArray,index=range(0,len(newArray)))

def SubValue(listOfIndex,listOfVal):
    newArray = []
    for index in listOfIndex:
        newArray.append(listOfVal[int(index)])
    return newArray

def generateFrac(numOfFac,BoundingBox):
    RandomGeneratedList = pyDOE.ff2n(numOfFac)
    for j in range(0,numOfFac):
        MinVal = BoundingBox[2*j]
        MaxVal = BoundingBox[2*j+1]
        
        for i in range(0,len(RandomGeneratedList)):
            val = RandomGeneratedList[i][j]
            if(val == 1):
                RandomGeneratedList[i][j] = MaxVal
            elif(val == -1):
                RandomGeneratedList[i][j] = MinVal
            else:
                RandomGeneratedList[i][j] = None
    
    return RandomGeneratedList