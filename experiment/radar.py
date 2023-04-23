from awips.dataaccess import DataAccessLayer
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import numpy as np
from cartopy.mpl.gridliner import LONGITUDE_FORMATTER, LATITUDE_FORMATTER

DataAccessLayer.changeEDEXHost("edex-cloud.unidata.ucar.edu")

# dataTypes = DataAccessLayer.getSupportedDatatypes()
# dataTypes.sort()
# print(dataTypes)

request = DataAccessLayer.newDataRequest("radar")
# available_locs = DataAccessLayer.getAvailableLocationNames(request)
# available_locs.sort()
# print(available_locs)

request.setLocationNames("kdmx")
availableParms = DataAccessLayer.getAvailableParameters(request)
availableParms.sort()
# print(availableParms)

# optionalIdents = DataAccessLayer.getOptionalIdentifiers(request)
# optionalIdents.sort()
# print(optionalIdents)

# requiredIdents = DataAccessLayer.getRequiredIdentifiers(request)
# requiredIdents.sort()
# print(requiredIdents)

productIDs = DataAccessLayer.getRadarProductIDs(availableParms)
productNames = DataAccessLayer.getRadarProductNames(availableParms)
print(productIDs)
print(productNames)

nexrad_data = {}

productNames = ['Reflectivity', 'Velocity']

def make_map(bbox, projection=ccrs.PlateCarree()):
    fig, ax = plt.subplots(figsize=(16, 16),
                           subplot_kw=dict(projection=projection))
    ax.set_extent(bbox)
    ax.coastlines(resolution='50m')
    gl = ax.gridlines(draw_labels=True)
    gl.top_labels = gl.right_labels = False
    gl.xformatter = LONGITUDE_FORMATTER
    gl.yformatter = LATITUDE_FORMATTER
    return fig, ax

def print_product(grid, flat, data):
    print('Product :', str(grid.getParameter()))
    print('Level   :', grid.getLevel())
    print('Time    :', str(grid.getDataTime()))
    print('Name    :', str(grid.getLocationName()))
    print('Range   :', np.nanmin(flat), " to ", np.nanmax(flat), " (Unit :", grid.getUnit(), ")")
    print('Size    :', str(data.shape))
    print()

def plot_product(lons, lats, data, grid, product):
    cmap = plt.get_cmap('rainbow')
    bbox = [lons.min()-0.5, lons.max()+0.5, lats.min()-0.5, lats.max()+0.5]
    fig, ax = make_map(bbox=bbox)
    cs = ax.pcolormesh(lons, lats, data, cmap=cmap)
    cbar = fig.colorbar(cs, extend='both', shrink=0.5, orientation='horizontal')
    cbar.set_label(grid.getParameter() +" " + grid.getLevel() + " " \
                   + grid.getLocationName() + " (" + product + "), (" + grid.getUnit() + ") " \
                   + "valid " + str(grid.getDataTime().getRefTime()))
    plt.show()

def plural_ending(count):
    if count != 1:
        return 's'
    return ''

def print_plural(count, desc):
    print(str(count) + ' ' + desc + plural_ending(count))

for product in productNames:
    print()
    print(product)

    request = DataAccessLayer.newDataRequest("radar")
    request.setLocationNames("kdmx")

    request.setParameters(product)
    availableLevels = DataAccessLayer.getAvailableLevels(request)
    availableLevels.sort()
    print_plural(len(availableLevels), 'available level')

    if not availableLevels:
        print("No levels found for " + product)
        continue

    times = DataAccessLayer.getAvailableTimes(request)
    print_plural(len(times), 'available time')

    if not times:
        print("No times found for " + product)
        continue

    for level in availableLevels:
        print()
        print(level)
        request.setLevels(level)

        times = DataAccessLayer.getAvailableTimes(request)
        print_plural(len(times), "available time")
        print(times[-1])

        response = DataAccessLayer.getGridData(request, [times[-1]])
        print("Recs : ", len(response))

        for grid in response:
            data = grid.getRawData()
            lons, lats = grid.getLatLonCoords()

            # print(lons)
            # print(lats)
            # print(data)

            nexrad_data[product] = data
            flat = np.ndarray.flatten(data)

            print_product(grid, flat, data)
            plot_product(lons, lats, data, grid, product)

