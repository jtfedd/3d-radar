from download_maps import loadCounties, loadStates
from file_util import openOrCreate
from render_maps import render
from roads import simplfyRoads

render(openOrCreate("states", loadStates), 2, "states")
render(openOrCreate("counties", loadCounties), 1, "counties")
render(openOrCreate("roads_simple", simplfyRoads), 1, "roads")
