#version 330

uniform mat4 p3d_ViewMatrixInverse;
uniform mat4 p3d_ProjectionMatrixInverse;
uniform vec2 resolution;

out vec4 p3d_FragColor;

void main() {
    float x = (2.0f * gl_FragCoord.x) / resolution.x - 1.0f;
    float y = 1.0f - (2.0f * gl_FragCoord.y) / resolution.y;
    float z = 1.0f;
    
    vec3 ray_nds = vec3(x, y, z);
    vec4 ray_clip = vec4(ray_nds.xy, -1.0, 1.0);
    vec4 ray_eye = p3d_ProjectionMatrixInverse * ray_clip;
    ray_eye = vec4(ray_eye.xy, -1.0, 0.0);

    vec3 ray_world = (p3d_ViewMatrixInverse * ray_eye).xyz;
    ray_world = normalize(ray_world);

    p3d_FragColor = vec4(abs(ray_world.x), abs(ray_world.y), abs(ray_world.z), 1.0);
}