from typing import List

from panda3d.core import (
    Geom,
    GeomLinestripsAdjacency,
    GeomNode,
    GeomVertexData,
    GeomVertexFormat,
    GeomVertexWriter,
    Vec3,
)


class Segments:
    def __init__(self, size: int) -> None:
        self.vdata = GeomVertexData("name", GeomVertexFormat.getV3(), Geom.UHStatic)
        self.vdata.setNumRows(size)

        self.vertex = GeomVertexWriter(self.vdata, "vertex")
        self.prim = GeomLinestripsAdjacency(Geom.UH_static)

        self.index = 0

    def addLoop(self, loop: List[Vec3]) -> None:
        self.prim.addVertex(self.index + len(loop) - 1)

        for i, point in enumerate(loop):
            self.vertex.addData3(point)
            self.prim.addVertex(i)

        self.prim.addVertex(self.index)
        self.prim.addVertex(self.index + 1)
        self.prim.closePrimitive()

        self.index += len(loop)

    def create(self) -> GeomNode:
        geom = Geom(self.vdata)
        geom.addPrimitive(self.prim)

        node = GeomNode("alert-boundary")
        node.addGeom(geom)

        return node
