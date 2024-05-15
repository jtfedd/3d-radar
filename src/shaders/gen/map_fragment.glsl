#version 330

// Inputs
uniform vec4 p3d_ColorScale;
uniform float clip_z;

// World-space vertex position passed in from vertex shader
in vec4 vpos;

// Outputs to Panda3D
out vec4 p3d_FragColor;

void main() {
  if (vpos.z < clip_z) {
    discard;
  }

  p3d_FragColor = p3d_ColorScale;
}