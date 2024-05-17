from direct.showbase.ShowBase import ShowBase
from panda3d.core import LineSegs, NodePath, Shader, TransparencyAttrib

base = ShowBase()

segs = LineSegs()
segs.moveTo(0, 0, 0)
segs.drawTo(1, 0, 0)
segs.setColor(1, 0, 0, 1)
segs.drawTo(1, 1, 0)
segs.setColor(0, 1, 1, 1)
segs.drawTo(-1, 1, 0)
segs.setThickness(10)
np = NodePath(segs.create())

np.setShader(
    Shader.load(
        Shader.SL_GLSL,
        vertex="shaders/line_v.glsl",
        geometry="shaders/line_g.glsl",
        fragment="shaders/line_f.glsl",
    )
)

np.setShaderInputs(
    viewport_size=(base.win.getXSize(), base.win.getYSize()),
    line_width=5,
    aa_radius=0,
)


np.reparentTo(base.render)
base.run()
