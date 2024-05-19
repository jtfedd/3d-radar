#version 330

uniform vec4 p3d_ColorScale;
out vec4 p3d_FragColor;
      
in vec4 geometry_color;

void main() {
    p3d_FragColor = geometry_color * p3d_ColorScale;
}