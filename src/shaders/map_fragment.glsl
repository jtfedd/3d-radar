#version 330

// Inputs
uniform vec4 p3d_ColorScale;
uniform float clip_z;

$inputs

// World-space vertex position from geometry shader
in vec3 gpos;

// Outputs to Panda3D
out vec4 p3d_FragColor;

#include map_util.part.glsl
      
void main() {
    // Cull backface segments
    if (backface(gpos)) {
        discard;
    }

    float factor = 1.0;

    if (gpos.z < clip_z) {
        factor = 0.6;
    }

    p3d_FragColor = p3d_ColorScale * factor;
}