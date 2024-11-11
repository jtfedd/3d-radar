void sphere_intersection(
    in vec3 center, in float r,
    in vec3 p, in vec3 v,
    out vec2 tRange, out bool no_intersection
) {
    vec3 CX = normalize(v);
    vec3 CS = center - p;

    float a = dot(CX, CX);
    float b = -2.0 * dot(CX, CS);
    float c = dot(CS, CS) - r * r;

    float discriminant = b * b - 4.0 * a * c;

    no_intersection = discriminant < 0.0;
    if (no_intersection) return;

    tRange = vec2(
        (-b - sqrt(discriminant)) / (2.0 * a),
        (-b + sqrt(discriminant)) / (2.0 * a)
    );
}