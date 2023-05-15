from panda3d.core import GeomVertexData
from panda3d.core import GeomVertexFormat
from panda3d.core import GeomTriangles
from panda3d.core import GeomNode
from panda3d.core import GeomEnums
from panda3d.core import Geom


# Take oriented vertices and triangles and generate Panda3D geometry
def trianglesToGeometry(vertices, triangles):
    vertexData = GeomVertexData("vdata", GeomVertexFormat.getV3n3(), Geom.UHStatic)
    vertexData.uncleanSetNumRows(len(vertices))
    vertexDataArray = vertexData.modifyArray(0)
    vertexDataView = memoryview(vertexDataArray).cast("B").cast("f")
    vertexDataView[:] = vertices.flatten()

    trianglesData = GeomTriangles(Geom.UHStatic)
    trianglesData.setIndexType(GeomEnums.NT_uint16)
    trianglesDataArray = trianglesData.modifyVertices()
    trianglesDataArray.uncleanSetNumRows(len(triangles) * 3)
    trianglesDataView = memoryview(trianglesDataArray).cast("B").cast("H")
    trianglesDataView[:] = triangles.flatten()

    geom = Geom(vertexData)
    geom.addPrimitive(trianglesData)

    node = GeomNode("gnode")
    node.addGeom(geom)

    return node
