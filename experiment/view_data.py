from direct.showbase.ShowBase import ShowBase
import pickle
import os
import numpy as np

from src.gradient import gradient

dmxLong = -93.7228499
dmxLat = 41.731099999999998

scriptDir = os.path.abspath(os.path.dirname(__file__))
dataDir = os.path.join(scriptDir, 'cached_data')

def print_product(grid, flat, data):
    print('Product :', str(grid.getParameter()))
    print('Level   :', grid.getLevel())
    print('Time    :', str(grid.getDataTime()))
    print('Name    :', str(grid.getLocationName()))
    print('Range   :', np.nanmin(flat), " to ", np.nanmax(flat), " (Unit :", grid.getUnit(), ")")
    print('Size    :', str(data.shape))
    print()

class Viewer(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)

        fileName = 'Reflectivity_05TILT_2023-03-11_141336.pickle'
        filePath = os.path.join(dataDir, fileName)
        with open(filePath, 'rb') as f:
            data = pickle.load(f)
        print('Read', filePath)

        grid = data[0]
        raw = grid.getRawData()
        lons, lats = grid.getLatLonCoords()
        lons = np.ndarray.flatten(lons)
        lats = np.ndarray.flatten(lats)
        flat = np.ndarray.flatten(raw)

        print(len(lons), len(lats), len(flat))

        print(flat)

        print_product(grid, flat, raw)

        minVal = np.nanmin(flat)
        maxVal = np.nanmax(flat)

        count = 0
        countNotNan = 0
        for val in flat:
            count += 1
            if not np.isnan(val):
                countNotNan += 1
        print(count, countNotNan)

        x = 0
        radarBase = self.render.attachNewNode("radar" + str(x))

        for i in range(len(flat)):
            if i % 100000 == 0:
                print(i)
                radarBase.clearModelNodes()
                radarBase.flattenStrong()

                x += 1
                radarBase = self.render.attachNewNode("radar" + str(x))

            if i % 29 != 0:
                continue

            val = flat[i]

            if np.isnan(val):
                continue

            longitude = lons[i] - dmxLong
            latitude = lats[i] - dmxLat

            cube = self.loader.loadModel("assets/cube.glb")
            cube.reparentTo(radarBase)
            cube.setPos(latitude, longitude, 0)
            cube.setColorScale(gradient(minVal, maxVal, val))
            cube.setScale(0.01)


app = Viewer()
app.run()
