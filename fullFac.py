# -*- coding: utf-8 -*-
"""
Created on Fri Mar 16 17:11:17 2018

@author: inst
"""

import pyDOE

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
            
    
    
if __name__=="__main__":
    numOfFac = 3
    BoundingBox = [10,100,150,200,10,50]
    result=generateFrac(numOfFac, BoundingBox)
    print(result)