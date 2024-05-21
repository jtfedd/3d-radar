#version 330

// Inputs
uniform vec4 p3d_ColorScale;
uniform float clip_z;

// World-space vertex position from geometry shader
in vec4 gpos;

// Outputs to Panda3D
out vec4 p3d_FragColor;
      
void main() {
    if (gpos.z < clip_z) {
        discard;
    }

    p3d_FragColor = p3d_ColorScale;
}