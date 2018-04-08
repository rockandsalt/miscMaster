# -*- coding: utf-8 -*-
"""
Created on Fri Mar 16 17:11:17 2018

@author: inst
"""

import pyDOE

from helperFunction.Func import generateFrac


if __name__=="__main__":
    numOfFac = 3
    BoundingBox = [10,100,150,200,10,50]
    result=generateFrac(numOfFac, BoundingBox)
    print(result)