#version 330

// Vertex inputs
in vec4 p3d_Vertex;

// Vertex outputs
out vec4 vpos;

// Uniform inputs
uniform mat4 p3d_ModelViewProjectionMatrix;
uniform mat4 p3d_ModelMatrix;

// Main function
void main() {
    vpos = p3d_ModelMatrix * p3d_Vertex;
    gl_Position = p3d_ModelViewProjectionMatrix * p3d_Vertex;
}
