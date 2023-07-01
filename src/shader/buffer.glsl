#version 460

uniform samplerBuffer databuffer;

uniform sampler2D scene;

out vec4 p3d_FragColor;

void main() {
    vec4 scene_color = texelFetch(scene, ivec2(gl_FragCoord.xy), 0);
    float value = texelFetch(databuffer, int(gl_FragCoord.x + gl_FragCoord.y)).r;
    p3d_FragColor = scene_color * (1 - value) + vec4(value, value, value, value);
}