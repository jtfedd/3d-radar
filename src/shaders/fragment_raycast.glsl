#version 460

// Inputs from Panda3D
uniform mat4 p3d_ViewMatrixInverse;
uniform mat4 p3d_ProjectionMatrixInverse;

// Inputs from program
uniform vec2 resolution;

uniform mat4 trans_world_to_model_of_camera;
uniform mat4 projection_matrix_inverse;

uniform sampler2D scene;

// Outputs to Panda3D
out vec4 p3d_FragColor;

vec3 gen_ray_from_params() {
    float x = (2.0 * gl_FragCoord.x) / resolution.x - 1.0;
    float y = (2.0 * gl_FragCoord.y) / resolution.y - 1.0;
    
    vec4 ray_clip = vec4(x, y, -1.0, 1.0);
    vec4 ray_eye = p3d_ProjectionMatrixInverse * ray_clip;
    ray_eye = vec4(ray_eye.xy, -1.0, 0.0);

    vec3 ray_world = (p3d_ViewMatrixInverse * ray_eye).xyz;
    ray_world = normalize(ray_world);

    return ray_world;
}

vec3 gen_ray_from_input() {
    float x = (2.0 * gl_FragCoord.x) / resolution.x - 1.0;
    float y = (2.0 * gl_FragCoord.y) / resolution.y - 1.0;
    
    vec4 ray_clip = vec4(x, y, -1.0, 1.0);
    vec4 ray_eye = (projection_matrix_inverse * ray_clip);
    ray_eye = vec4(ray_eye.xyz, 0.0);

    vec3 ray_world = (inverse(trans_world_to_model_of_camera) * ray_eye).xyz;
    ray_world = normalize(ray_world);

    return ray_world;
}

vec4 blend_onto(vec4 front, vec4 behind) {
    return front + (1.0 - front.a) * behind;
}

vec4 ray_color(in vec3 rd) {
    return vec4(rd.x, rd.y, rd.z, 0.5);
}

void main() {
    vec4 scene_color = texelFetch(scene, ivec2(gl_FragCoord.xy), 0);

    vec3 ray_from_params = gen_ray_from_params();
    vec3 ray_from_input = gen_ray_from_input();

    vec4 rc = ray_color(ray_from_params);
    if (gl_FragCoord.x > (resolution.x / 2)) {
        rc = ray_color(ray_from_input);
    }

    p3d_FragColor = blend_onto(rc, scene_color);
}
