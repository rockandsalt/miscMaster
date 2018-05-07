import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit

import mysql.connector as mariadb
from helperFunction.secret import DBAccess

def CreateDataDB(DataFrame, EID):
    mariadb_connection = mariadb.connect(user='root', password=DBAccess['root'], database='mysql')
    cursor = mariadb_connection.cursor()

    for index, row in DataFrame.iterrows():
        cmd = """INSERT INTO pzthdodarrheometrydata 
                 VALUES ({},{},"sec",{},"C",{},{},"Pa",{},"mPas",{},"1/s");""".format(EID,row['Time'],row['Temp'],
                 row['Shear'],row['Shear Stress'],row['Viscosity'],row['rate'])

        cursor.execute(cmd)

    mariadb_connection.commit()
    mariadb_connection.close()

def PowerLaw(shearRate,k,n):
    return k*shearRate**n

def Herschel_Bulkley(shearRate,YieldStr, k, n):
    return YieldStr*k*shearRate**n

def Bingham(shearRate,yieldStr,plasticVisc):
    return yieldStr+plasticVisc*shearRate

def Casson(shearRate,yieldStr,plasticVisc):
    return (np.sqrt(yieldStr)+np.sqrt(plasticVisc*shearRate))**2

def RSquare(rdata,fdata):
    residuals = rdata - fdata
    ss_res = np.sum(residuals**2)
    ss_tot = np.sum((rdata-np.mean(rdata))**2)
    return 1-(ss_res/ss_tot)

if __name__ == "__main__":

    plt.rc('text',usetex=True)
    df = pd.read_excel("./bin/RInput.xlsx",sheetname="Sheet1")
    CreateDataDB(df,3)
    rate = df['rate'].values
    Viscosity = df['Viscosity'].values
    shearStress = df['Shear Stress'].values

    cassonCoef, cassonCov = curve_fit(Casson,rate,shearStress)
    CassonFitData = Casson(rate,*cassonCoef)
    CassonRsquare = RSquare(shearStress,CassonFitData)

    powerLawCoef, pwCov = curve_fit(PowerLaw,rate,shearStress)
    powerLawFitData = PowerLaw(rate,*powerLawCoef)
    powerLawRsquare = RSquare(shearStress,powerLawFitData)

    BinghamCoef, BingCov = curve_fit(Bingham,rate,shearStress)
    BinghamFitData = Bingham(rate,*BinghamCoef)
    BinghamRsquare = RSquare(shearStress,BinghamFitData)

    HBCoef, HBCov = curve_fit(Herschel_Bulkley,rate,shearStress)
    HBFitData = Herschel_Bulkley(rate,*HBCoef)
    HBRSquare = RSquare(shearStress,HBFitData)

    plt.plot(rate,shearStress, 'b*' , label = 'raw')
    plt.plot(rate,CassonFitData,'r--',label='Casson $r^2$={}'.format(CassonRsquare))
    plt.plot(rate,powerLawFitData,'g--',label = 'powerLaw $r^2$={}'.format(powerLawRsquare))
    plt.plot(rate,BinghamFitData,'c-',label='Bingham $r^2$={}'.format(BinghamRsquare))
    plt.plot(rate,HBFitData,'y--',label='Hershel Bulkley $r^2$={}'.format(HBRSquare))

    plt.xlabel(r'shear rate(s^{-1})')
    plt.ylabel(r'shear stress(cp)')
    plt.legend()
    plt.show()
    