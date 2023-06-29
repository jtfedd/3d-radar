import struct
from random import random

from direct.filter.FilterManager import FilterManager
from direct.showbase.ShowBase import ShowBase
from panda3d.core import GeomEnums, Shader, Texture

from lib.util.optional import unwrap

base = ShowBase()

SIZE = 3000000

print("Max buffer size: %d" % (base.win.get_gsg().get_max_buffer_texture_size()))

buffer = Texture("texbuffer")
buffer.setup_buffer_texture(SIZE, Texture.T_float, Texture.F_r32, GeomEnums.UH_dynamic)

manager = FilterManager(base.win, base.cam)  # type: ignore
plane = unwrap(manager.renderSceneInto())

plane.setShader(Shader.load(Shader.SL_GLSL, "shader/vertex.glsl", "shader/buffer.glsl"))
plane.setShaderInput("databuffer", buffer)


def rebuild_data():
    data = memoryview(buffer.modifyRamImage())
    for i in range(SIZE):
        data[i * 4 : i * 4 + 4] = struct.pack("f", random())


rebuild_data()
base.accept("r", rebuild_data)

base.run()
