import random

import numpy as np
from direct.filter.FilterManager import FilterManager
from direct.showbase.ShowBase import ShowBase
from panda3d.core import GeomEnums, Shader, Texture

from lib.util.optional import unwrap
from lib.util.util import defaultLight

base = ShowBase()

SIZE = 200000000

print("Max buffer size: %d" % (base.win.get_gsg().get_max_buffer_texture_size()))

base.setFrameRateMeter(True)

cube = unwrap(base.loader.loadModel("assets/cube.glb"))
cube.reparentTo(base.render)
defaultLight(base)


manager = FilterManager(base.win, base.cam)  # type: ignore
scene = Texture("scene")
plane = unwrap(manager.renderSceneInto(colortex=scene))

plane.setShader(Shader.load(Shader.SL_GLSL, "shader/vertex.glsl", "shader/buffer.glsl"))
plane.setShaderInput("scene", scene)

size = SIZE + random.randrange(0, 10000)
size2 = SIZE + random.randrange(0, 10000)
rand = np.random.uniform(0.0, 1.0, size).astype(np.float32).tobytes()
rand2 = np.random.uniform(0.0, 1.0, size2).astype(np.float32).tobytes()

buffer = Texture("texbuffer")
buffer.setup_buffer_texture(
    max(size, size2), Texture.T_float, Texture.F_r32, GeomEnums.UH_dynamic
)
plane.setShaderInput("databuffer", buffer)


def rebuild_data() -> None:
    r_size = size
    r_data = rand

    if random.randrange(0, 2) == 1:
        r_size = size2
        r_data = rand2

    data = memoryview(buffer.modifyRamImage())
    data[0 : r_size * 4] = r_data


rebuild_data()
base.accept("r", rebuild_data)

base.run()
