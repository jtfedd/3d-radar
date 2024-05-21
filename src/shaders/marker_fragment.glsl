#version 330

// Inputs
uniform vec4 p3d_ColorScale;

uniform struct p3d_LightModelParameters {
  vec4 ambient;
} p3d_LightModel;

uniform struct p3d_LightSourceParameters {
  // Primary light color.
  vec4 color;

  // View-space position.  If w=0, this is a directional light, with the xyz
  // being -direction.
  vec4 position;
} p3d_LightSource[1];

// Normal vector passed in from vertex shader
in vec3 normal;

// Outputs to Panda3D
out vec4 p3d_FragColor;

void main() {
  // Ambient
  vec4 ambient = p3d_LightModel.ambient;

  // Directional
  float diffStrength = max(dot(normal, p3d_LightSource[0].position.xyz), 0.0);
  vec4 diffuse = diffStrength * p3d_LightSource[0].color;

  p3d_FragColor = (ambient + diffuse) * p3d_ColorScale;
}