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

uniform float opacity;
uniform float threshold;
uniform float max_el_index;

$inputs

// World-space vertex position from vertex shader
in vec3 vpos;

// Outputs to Panda3D
out vec4 p3d_FragColor;

#include resolve_elevation.part.glsl
#include surface_sample_position.part.glsl
#include volume_sharp.part.glsl
#include color_util.part.glsl
#include surface_color.part.glsl
      
void main() {
    vec3 color = resolve_surface_color();
    p3d_FragColor = vec4(color.xyz, opacity);
}