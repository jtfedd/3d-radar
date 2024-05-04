// For each coord, return the range of t for which p+t*v is inside the box defined
// by the corners box_min and box_max, and whether the ray intersects the box.
// More on this method here: https://tavianator.com/2011/ray_box.html
void box_intersection(
    in vec3 box_min, in vec3 box_max,
    in vec3 p, in vec3 v,
    out vec2 tRange, out bool no_intersection
) {
    vec3 tb0 = (box_min - p) / v;
    vec3 tb1 = (box_max - p) / v;
    vec3 tmin = min(tb0, tb1);
    vec3 tmax = max(tb0, tb1);

    tRange = vec2(
        max(max(tmin.x, tmin.y), tmin.z),
        min(min(tmax.x, tmax.y), tmax.z)
    );

    no_intersection = tRange.t < tRange.s;
}