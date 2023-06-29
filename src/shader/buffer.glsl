#version 460

uniform samplerBuffer databuffer;

out vec4 p3d_FragColor;

void main() {
    float value = texelFetch(databuffer, int(gl_FragCoord.x + gl_FragCoord.y)).r;
    p3d_FragColor = vec4(value, value, value, 1.0);
}