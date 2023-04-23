from awips.dataaccess import DataAccessLayer
import pickle
from pathlib import Path
import os

site = "kdmx"
productNames = ['Reflectivity', 'Velocity']

DataAccessLayer.changeEDEXHost("edex-cloud.unidata.ucar.edu")

scriptDir = os.path.abspath(os.path.dirname(__file__))
dataDir = os.path.join(scriptDir, 'cached_data')

for product in productNames:
    print()
    print(product)

    request = DataAccessLayer.newDataRequest("radar")
    request.setLocationNames(site)
    request.setParameters(product)

    availableLevels = DataAccessLayer.getAvailableLevels(request)
    availableLevels.sort()

    for level in availableLevels:
        print()
        print(level)
        request.setLevels(level)

        times = DataAccessLayer.getAvailableTimes(request)

        for i in range(0, min(len(times), 10)):
            time = times[-(i+1)]
            dataName = product + ' ' + str(level) + ' ' + str(time)
            dataName = dataName.replace(' ', '_')
            dataName = dataName.replace('.', '')
            dataName = dataName.replace(':', '')
            print(dataName)

            response = DataAccessLayer.getGridData(request, [time])
            print('Got response')

            fileName = dataName + '.pickle'
            filePath = os.path.join(dataDir, fileName)
            with open(filePath, 'wb') as f:
                pickle.dump(response, f, pickle.HIGHEST_PROTOCOL)
            print('Wrote', filePath)
