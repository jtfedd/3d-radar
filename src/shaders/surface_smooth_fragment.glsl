#version 330

#define MAX_SCANS 20
$constants

// Inputs
uniform vec3 earth_center;

uniform int scan_count[1];
uniform float elevation[MAX_SCANS];
uniform float az_step[MAX_SCANS];
uniform float az_count[MAX_SCANS];
uniform float r_first[MAX_SCANS];
uniform float r_step[MAX_SCANS];
uniform int r_count[MAX_SCANS];
uniform int offset[MAX_SCANS];

uniform float density_params[7];

uniform usamplerBuffer volume_data;

$inputs

#include resolve_elevation.part.glsl
#include volume_smooth.part.glsl
#include color_util.part.glsl

// World-space vertex position from vertex shader
in vec3 vpos;

// Outputs to Panda3D
out vec4 p3d_FragColor;
      
void main() {
    if (scan_count[0] < 3) discard;

    float sample_value = data_value_for_sweep(vpos, 1);
    if (sample_value < 0.1) discard;
    
    vec3 sample_color = colorize(sample_value);

    p3d_FragColor = vec4(sample_color.xyz, 1.0);
}