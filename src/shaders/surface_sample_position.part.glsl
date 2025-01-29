vec3 resolve_surface_sample_position(vec3 surface_pos, int sweep_index) {
    vec3 ray = surface_pos - earth_center;
    vec3 up = -earth_center;
    float center_angle = acos(dot(ray, up)/ (length(ray) * length(up)));
    float x_angle = (PI / 2.0) + elevation[sweep_index];
    float a_angle = PI - x_angle - center_angle;
    float a = length(up);
    float x = (a / sin(a_angle)) * sin(x_angle);
    vec3 sample_pos = earth_center + (normalize(ray)*x);
    return sample_pos;
}