import requests
import shapefile
import shapely
import shapely.geometry
import shapely.geometry.base
import shapely.ops

HOST = "https://www2.census.gov/geo/tiger/"

COUNTY_RAW = "TIGER2023/COUNTY/tl_2023_us_county.zip"
COUNTY_500K = "GENZ2022/shp/cb_2022_us_county_500k.zip"
COUNTY_5M = "GENZ2022/shp/cb_2022_us_county_5m.zip"
COUNTY_20M = "GENZ2022/shp/cb_2022_us_county_20m.zip"

STATE_RAW = "TIGER2023/STATE/tl_2023_us_state.zip"
STATE_500K = "GENZ2022/shp/cb_2022_us_state_500k.zip"
STATE_5M = "GENZ2022/shp/cb_2022_us_state_5m.zip"
STATE_20M = "GENZ2022/shp/cb_2022_us_state_20m.zip"

ROADS = "TIGER2023/PRISECROADS/tl_2023_{0:02d}_prisecroads.zip"


def loadStates() -> shapely.geometry.base.BaseGeometry:
    filename = HOST + STATE_500K
    print("Downloading", filename)
    shape = shapely.geometry.shape(shapefile.Reader(filename).shapes())
    return shape


def loadCounties() -> shapely.geometry.base.BaseGeometry:
    filename = HOST + COUNTY_500K
    print("Downloading", filename)
    shape = shapely.geometry.shape(shapefile.Reader(filename).shapes())
    return shape


def loadRoads() -> shapely.geometry.base.BaseGeometry:
    filenameFmt = HOST + ROADS
    fileCount = 80
    roads = []
    for i in range(fileCount):
        filename = filenameFmt.format(i)
        print("Downloading", filename)
        r = requests.head(filename, allow_redirects=True, timeout=10)
        if r.status_code == 404:
            print("Does not exist")
            continue

        shape = shapely.geometry.shape(shapefile.Reader(filename).shapes())
        roads.append(shape)

    return shapely.geometry.GeometryCollection(roads)
