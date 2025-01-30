#version 330

// Vertex inputs
in vec4 p3d_Vertex;

// Vertex outputs
out vec3 vpos;

// Uniform inputs
uniform mat4 p3d_ModelMatrix;
uniform mat4 p3d_ModelViewProjectionMatrix;

void main() {
    vpos = (p3d_ModelMatrix * p3d_Vertex).xyz;
    gl_Position = p3d_ModelViewProjectionMatrix * p3d_Vertex;
}
