#version 150

uniform vec4 p3d_ColorScale;

in vec4 g_color;

out vec4 p3d_FragColor;

void main(void) {
	p3d_FragColor = g_color * p3d_ColorScale;
}