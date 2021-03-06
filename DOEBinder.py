import pyDOE as doe
import numpy as np
import pandas as pd
from helperFunction.Func import createSeries

if __name__ == "__main__":
    layerThickness = range(150,225,25)
    linearVelocity = [25,50,75]
    rot = range(10,180,30)

    num = [len(layerThickness),len(linearVelocity),len(rot)]
    spread = np.array(doe.fullfact(num))
    
    layerThicknessSeries = createSeries(spread[0:,0],layerThickness)
    linearVelocitySeries = createSeries(spread[0:,1],linearVelocity)
    rotSeries = createSeries(spread[0:,2], rot)

    d = {'layer_thickness':layerThicknessSeries,'linear_velocity':linearVelocitySeries, 'rotation': rotSeries}

    df = pd.DataFrame(d)

    writer = pd.ExcelWriter('./bin/BinderJet.xlsx')
    df.to_excel(writer,'Sheet1')
    writer.save()
    print(df)