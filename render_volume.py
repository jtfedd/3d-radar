from direct.showbase.ShowBase import ShowBase
import numpy as np

from src.gradient import gradient
from src.data_connector.data_connector import DataConnector
from src.data_connector.request import Request

import datetime

def get_data():
    site = 'KVWX'
    date = datetime.date(year=2019, month=6, day=26)
    time = datetime.time(hour=22, minute=11, second=5)

    request = Request(site, date, time)

    return DataConnector().load(request)
    
def process_sweep(base, sweep, radarBase, minVal, maxVal):
    for ray in sweep:
        process_ray(base, ray, radarBase, minVal, maxVal)

def process_ray(base, ray, radarBase, minVal, maxVal):
    header = ray[0]

    azimuth = header.az_angle
    elevation = header.el_angle

    ref_header = ray[4][b'REF'][0]
    ref_range = np.arange(ref_header.num_gates) * ref_header.gate_width + ref_header.first_gate

    cos_el = np.cos(np.deg2rad(elevation))
    sin_el = np.sin(np.deg2rad(elevation))

    cos_az = np.cos(np.deg2rad(azimuth))
    sin_az = np.sin(np.deg2rad(azimuth))

    for i, value in enumerate(ray[4][b'REF'][1]):
        if np.isnan(value):
            continue

        rng = ref_range[i]

        x = rng * cos_el * sin_az
        y = rng * cos_el * cos_az
        z = rng * sin_el

        cube = base.loader.loadModel("assets/cube.glb")
        cube.reparentTo(radarBase)
        cube.setPos(x, y, z)
        cube.setColorScale(gradient(minVal, maxVal, value))

def process_min_max(f):
    minValue = f.sweeps[0][0][4][b'REF'][1][0]
    maxValue = f.sweeps[0][0][4][b'REF'][1][0]

    for sweep in f.sweeps:
        for ray in sweep:
            for value in ray[4][b'REF'][1]:
                if value < minValue:
                    minValue = value
                if value > maxValue:
                    maxValue = value

    return minValue, maxValue
    

class Viewer(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)
        radarBase = self.render.attachNewNode("radar")

        f = get_data()

        minVal, maxVal = process_min_max(f)

        for sweep in f.sweeps:
            process_sweep(self, sweep, radarBase, minVal, maxVal)

        radarBase.clearModelNodes()
        radarBase.flattenStrong()


app = Viewer()
app.run()
