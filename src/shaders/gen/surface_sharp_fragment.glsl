#version 330

// Inputs



// World-space vertex position from vertex shader
in vec3 vpos;

// Outputs to Panda3D
out vec4 p3d_FragColor;
      
void main() {
    p3d_FragColor = vec4(vpos.xyz, 1.0);
}