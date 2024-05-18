#version 330

in vec4 p3d_Vertex;
in vec4 p3d_Color;

uniform mat4 p3d_ModelViewProjectionMatrix;

out vec4 vertex_color;

void main() {
    vertex_color = p3d_Color;
    gl_Position = p3d_ModelViewProjectionMatrix * p3d_Vertex;
}