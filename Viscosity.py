import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit

import mysql.connector as mariadb
from helperFunction.secret import DBAccess


if __name__ == "__main__":
    mariadb_connection = mariadb.connect(user='root', password=DBAccess['root'], database='mysql')
    cursor = mariadb_connection.cursor()

    plt.rc('text',usetex=True)
    
    fig = plt.figure()
    ax = fig.add_subplot(111)
    label = ['r*','g*','b*','y*']
    count = 0
    for i in [9,5,10,12]:
        command = """SELECT pzthdodarrheometrydata.ShearRate,pzthdodarrheometrydata.Viscosity 
                    FROM pzthdodarrheometrydata
                    JOIN pzthdodarheometerexperiment ON pzthdodarrheometrydata.ExperimentID = pzthdodarheometerexperiment.ID
                    WHERE pzthdodarheometerexperiment.RecipeID={};""".format(str(i))
        
        cursor.execute(command)
        listShearRate = []
        listViscosity = []

        for (ShearRate,Viscosity) in cursor:
            if(Viscosity < 100):
                listShearRate.append(ShearRate)
                listViscosity.append(Viscosity)
        
        ax.plot(listShearRate,listViscosity,label[count],label = 'R {}'.format(str(i)))

        count = count + 1

    plt.xlabel(r'shear rate(s^{-1})')
    plt.ylabel(r'viscosity(Pa.s)')
    plt.title('Viscosity versus Shear rate')
    plt.legend()
    plt.show()
    


        