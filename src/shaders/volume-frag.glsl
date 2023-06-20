#version 330

uniform mat4 p3d_ViewMatrixInverse;
uniform mat4 p3d_ProjectionMatrixInverse;
uniform vec2 resolution;
uniform vec3 camera_position;

out vec4 p3d_FragColor;

vec3 gen_ray() {
    float x = (2.0f * gl_FragCoord.x) / resolution.x - 1.0f;
    float y = (2.0f * gl_FragCoord.y) / resolution.y - 1.0f;
    float z = 1.0f;
    
    vec3 ray_nds = vec3(x, y, z);
    vec4 ray_clip = vec4(ray_nds.xy, -1.0, 1.0);
    vec4 ray_eye = p3d_ProjectionMatrixInverse * ray_clip;
    ray_eye = vec4(ray_eye.xy, -1.0, 0.0);

    vec3 ray_world = (p3d_ViewMatrixInverse * ray_eye).xyz;
    ray_world = normalize(ray_world);

    return ray_world;
}

float distance_from_sphere(in vec3 point, in vec3 center, float radius) {
    return length(point - center) - radius;
}

vec3 ray_march(in vec3 ro, in vec3 rd) {
    float total_distance_traveled = 0.0;
    const int NUMBER_OF_STEPS = 32;
    const float MINIMUM_HIT_DISTANCE = 0.001;
    const float MAXIMUM_TRACE_DISTANCE = 1000.0;

    for (int i = 0; i < NUMBER_OF_STEPS; ++i) {
        vec3 current_position = ro + total_distance_traveled * rd;

        float distance_to_closest = distance_from_sphere(current_position, vec3(0.0), 1.0);

        if (distance_to_closest < MINIMUM_HIT_DISTANCE) {
            return vec3(1.0, 0.0, 0.0);
        }

        if (total_distance_traveled > MAXIMUM_TRACE_DISTANCE) {
            break;
        }
        total_distance_traveled += distance_to_closest;
    }
    
    return vec3(0.0);
}

void main() {
    vec3 ro = camera_position;
    vec3 rd = gen_ray();

    vec3 shaded_color = ray_march(ro, rd);

    p3d_FragColor = vec4(shaded_color, 0.5);
}