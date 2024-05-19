from direct.showbase.ShowBase import ShowBase
from panda3d.core import (
    Geom,
    GeomLinestripsAdjacency,
    GeomNode,
    GeomVertexData,
    GeomVertexFormat,
    GeomVertexWriter,
    LineSegs,
    NodePath,
    Shader,
)

base = ShowBase()


def makeLineSegs() -> None:
    segs = LineSegs()
    segs.moveTo(0, 0, 0)
    segs.drawTo(1, 0, 0)
    segs.setColor(1, 0, 0, 1)
    segs.drawTo(1, 1, 0)
    segs.setColor(0, 1, 1, 1)
    segs.drawTo(-1, 1, 0)
    segs.setThickness(10)
    np = NodePath(segs.create())
    np.reparentTo(base.render)


def makeSmoothSegs() -> None:
    vdata = GeomVertexData("name", GeomVertexFormat.getV3c4(), Geom.UHStatic)
    vdata.setNumRows(4)

    vertex = GeomVertexWriter(vdata, "vertex")
    color = GeomVertexWriter(vdata, "color")

    vertex.addData3(0, 0, 0)
    color.addData4(1, 1, 1, 1)
    vertex.addData3(1, 0, 0)
    color.addData4(1, 1, 1, 1)
    vertex.addData3(1, 1, 0)
    color.addData4(1, 0, 0, 1)
    vertex.addData3(-1, 1, 0)
    color.addData4(0, 1, 1, 1)

    prim = GeomLinestripsAdjacency(Geom.UH_static)
    prim.addVertex(1)
    prim.addVertex(0)
    prim.addVertex(1)
    prim.addVertex(2)
    prim.addVertex(3)
    prim.addVertex(2)
    prim.closePrimitive()

    geom = Geom(vdata)
    geom.addPrimitive(prim)

    node = GeomNode("gnode")
    node.addGeom(geom)

    np = base.render.attachNewNode(node)

    np.setShader(
        Shader.load(
            Shader.SL_GLSL,
            vertex="shaders/line_v.glsl",
            geometry="shaders/line_g.glsl",
            fragment="shaders/line_f.glsl",
        )
    )

    np.setShaderInputs(
        window_size=(base.win.getXSize(), base.win.getYSize()),
        thickness=10,
    )

    # np.setRenderModeWireframe()
    # np.setColorScale(0.8, 0.8, 0.8, 1.0)


# makeLineSegs()
makeSmoothSegs()

base.run()
