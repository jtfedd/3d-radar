import numpy as np
import numpy.typing as npt
from panda3d.core import (
    Geom,
    GeomEnums,
    GeomNode,
    GeomTriangles,
    GeomVertexData,
    GeomVertexFormat,
)

from lib.geometry import normals_sharp, normals_smooth


def getGeometry(
    vertices: npt.NDArray[np.float32],
    triangles: npt.NDArray[np.uint32],
    smooth: bool = False,
) -> GeomNode:
    if smooth:
        vertices, triangles = normals_smooth.orientVertices(vertices, triangles)
    else:
        vertices, triangles = normals_sharp.orientVertices(vertices, triangles)

    return trianglesToGeometry(vertices, triangles)


# Take oriented vertices and triangles and generate Panda3D geometry
def trianglesToGeometry(
    vertices: npt.NDArray[np.float32], triangles: npt.NDArray[np.uint32]
) -> GeomNode:
    vertexData = GeomVertexData("vdata", GeomVertexFormat.getV3n3(), Geom.UHStatic)
    vertexData.uncleanSetNumRows(len(vertices))
    vertexDataArray = vertexData.modifyArray(0)
    vertexDataView = memoryview(vertexDataArray).cast("B").cast("f")
    vertexDataView[:] = vertices.flatten().astype(dtype=np.float32)

    trianglesData = GeomTriangles(Geom.UHStatic)
    trianglesData.setIndexType(GeomEnums.NT_uint32)
    trianglesDataArray = trianglesData.modifyVertices()
    trianglesDataArray.uncleanSetNumRows(len(triangles) * 3)
    trianglesDataView = memoryview(trianglesDataArray).cast("B").cast("I")

    trianglesFlat = triangles.flatten().astype(dtype=np.uint32)
    trianglesView = memoryview(trianglesFlat).cast("B").cast("I")

    trianglesDataView[:] = trianglesView

    geom = Geom(vertexData)
    geom.addPrimitive(trianglesData)

    node = GeomNode("gnode")
    node.addGeom(geom)

    return node
