#version 330

// Inputs
uniform vec4 p3d_ColorScale;
uniform float clip_z;

uniform vec3 world_pos;
uniform vec3 camera_pos;

// World-space vertex position from geometry shader
in vec3 gpos;

// Outputs to Panda3D
out vec4 p3d_FragColor;


bool backface(vec3 pos) {
    return dot((pos - camera_pos), (pos - world_pos)) > 0;
}
      
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