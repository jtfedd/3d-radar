from panda3d.core import Point2, Point3

from lib.app.context import AppContext


def map3dToAspect2d(
    ctx: AppContext,
    point: Point3,
) -> Point3 | None:
    """Maps the indicated 3-d point (a Point3), which is relative to
    the indicated NodePath, to the corresponding point in the aspect2d
    scene graph. Returns the corresponding Point3 in aspect2d.
    Returns None if the point is not onscreen."""

    # Convert the point to the 3-d space of the camera
    p3 = ctx.base.cam.getRelativePoint(ctx.base.render, point)
    # Convert it through the lens to render2d coordinates
    p2 = Point2()
    if not ctx.base.cam.node().getLens().project(p3, p2):
        return None
    r2d = Point3(p2[0], 0, p2[1])
    # And then convert it to aspect2d coordinates
    a2d = ctx.base.aspect2dp.getRelativePoint(ctx.base.render2dp, r2d)
    return a2d
