import datetime
import test.testutils.profile as mem_prof

import pynexrad

MEM_PROF = False

if MEM_PROF:
    mem_prof.start()

start = datetime.datetime.now()

level2File = pynexrad.download_nexrad_file(
    pynexrad.FileMetadata("KDMX", 2022, 3, 5, "KDMX20220305_233003_V06")
)

print(datetime.datetime.now(), "done")

print(datetime.datetime.now() - start)

if MEM_PROF:
    mem_prof.stop()

print(level2File.reflectivity.data)
print(level2File.reflectivity.meta)

print(len(level2File.velocity.data))
print(len(level2File.velocity.meta))
