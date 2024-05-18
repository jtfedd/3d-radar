#version 150

uniform vec4 p3d_ColorScale;
out vec4 p3d_FragColor;

void main(void) {
	p3d_FragColor = p3d_ColorScale;
}