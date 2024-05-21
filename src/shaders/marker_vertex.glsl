#version 330

// Vertex inputs
in vec4 p3d_Vertex;
in vec3 p3d_Normal;

// Vertex outputs
out vec3 normal;

// Uniform inputs
uniform mat4 p3d_ModelViewProjectionMatrix;
uniform mat3 p3d_NormalMatrix;

// Main function
void main() {
    normal = normalize(p3d_NormalMatrix * p3d_Normal);
    gl_Position = p3d_ModelViewProjectionMatrix * p3d_Vertex;
}
