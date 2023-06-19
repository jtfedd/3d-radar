#version 330

// Vertex inputs
in vec4 p3d_Vertex;

// Uniform inputs
uniform mat4 p3d_ModelViewProjectionMatrix;

// Main function
void main() {
    gl_Position = p3d_ModelViewProjectionMatrix * p3d_Vertex;
}