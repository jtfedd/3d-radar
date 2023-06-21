#version 330

uniform mat4 p3d_ViewMatrixInverse;
uniform mat4 p3d_ProjectionMatrixInverse;
uniform vec2 resolution;
uniform vec3 camera_position;

out vec4 p3d_FragColor;

const float NEAR = 1;
const float MAX_STEPS = 1000;
const float STEP_SIZE = 0.1; 

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

float density(in vec3 point, in vec3 center, float radius) {
    if (length(point - center) < radius) {
        return 1 - pow((length(point - center) / radius), 3);
    }

    return 0.0;
}

vec4 blendOnto(vec4 cFront, vec4 cBehind) {
    return cFront + (1.0 - cFront.a)*cBehind;
}

vec4 ray_march(in vec3 ro, in vec3 rd) {
    float transparency = 1.0f;
    vec4 color = vec4(0.0);

    for (int i = 0; i < MAX_STEPS; i++) {
        float sample_dist = NEAR + (i * STEP_SIZE);
        vec3 sample_pos = ro + sample_dist * rd;

        float sample_density = density(sample_pos, vec3(0.0), 2.0);
        float sample_attenuation = exp(-STEP_SIZE * sample_density);
        vec3 sample_color = vec3(1.0 - sample_density, 0, sample_density);
        float sample_alpha = sample_density * STEP_SIZE;

        vec4 ci = vec4(sample_color, 1.0) * sample_alpha;
        color = blendOnto(color, ci);
    }
    
    return color;
}

void main() {
    vec3 ro = camera_position;
    vec3 rd = gen_ray();

    vec4 shaded_color = ray_march(ro, rd);

    p3d_FragColor = shaded_color;
}