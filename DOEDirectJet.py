import pyDOE as doe
import numpy as np
import pandas as pd
from helperFunction.Func import SubValue
import mysql.connector as mariadb
from helperFunction.secret import DBAccess

if __name__ == "__main__":
    mariadb_connection = mariadb.connect(user='root', password=DBAccess['root'], database='mysql')

    cursor = mariadb_connection.cursor()

    PZTPercentwt = np.arange(40,80,10)
    MerpolAPercentwt = np.arange(0,15,5)
    PIPercentwt = np.arange(0.5,2.5,0.5)

    PIPercentwt = np.insert(PIPercentwt,0,0.1)

    num = [len(PZTPercentwt),len(MerpolAPercentwt),len(PIPercentwt)]
    spread = np.array(doe.fullfact(num))
    
    PZTPercentwtSeries = SubValue(spread[0:,0],PZTPercentwt)
    MerpolAPercentwtSeries = SubValue(spread[0:,1],MerpolAPercentwt)
    PIPercentwtSeries = SubValue(spread[0:,2], PIPercentwt)

    MaxVal = len(PZTPercentwtSeries)

    for i in range(0,MaxVal):
        PZT = PZTPercentwtSeries[i]
        MerpolA = MerpolAPercentwtSeries[i]
        PI = PIPercentwtSeries[i]
        HDODA = 100.0 - PZT - MerpolA - PI
        cmd = "INSERT INTO PZTRecipeHDODA VALUES (%d,%f,%f,%f,%f,%f);" % (i+1,PZT,HDODA,MerpolA,0,PI)
        cursor.execute(cmd)
    
    mariadb_connection.commit()

