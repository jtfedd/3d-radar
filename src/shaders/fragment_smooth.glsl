#version 330

#define MAX_SCANS 20
$constants

// Outputs to Panda3D
out vec4 p3d_FragColor;

// Inputs from program
uniform float time;

uniform sampler2D scene;
uniform sampler2D depth;

uniform vec2 resolution;
uniform vec3 camera_position;
uniform mat4 trans_world_to_model_of_camera;
uniform mat4 projection_matrix_inverse;

uniform vec3 bounds_start;
uniform vec3 bounds_end;

uniform int scan_count[1];
uniform float elevation[MAX_SCANS];
uniform float az_step[MAX_SCANS];
uniform float az_count[MAX_SCANS];
uniform float r_first[MAX_SCANS];
uniform float r_step[MAX_SCANS];
uniform int r_count[MAX_SCANS];
uniform int offset[MAX_SCANS];

uniform float density_params[7];

uniform samplerBuffer volume_data;

uniform float ambient_intensity;
uniform float directional_intensity;
uniform vec3 directional_orientation;
uniform bool volumetric_lighting;

$inputs

// End inputs

#define MIN_STEPS 5
#define MAX_STEPS 1000
#define STEP_SIZE 1.5

#define MIN_L_STEPS 5
#define MAX_L_STEPS 20
#define L_STEP_SIZE 1.5

#define ALPHA_CUTOFF 0.99

#include hash.part.glsl
#include box_intersection.part.glsl
#include color_util.part.glsl
#include density.part.glsl
#include resolve_elevation.part.glsl
#include volume_smooth.part.glsl
#include lightmarch.part.glsl
#include raymarch.part.glsl

void main() {
    vec4 scene_color = texelFetch(scene, ivec2(gl_FragCoord.xy), 0);
    vec4 depth_pixel = texelFetch(depth, ivec2(gl_FragCoord.xy), 0);

    vec2 uv = (gl_FragCoord.xy * 2.0) / resolution.xy - 1.0;
    float scaled_depth = depth_pixel.x * 2.0 - 1.0;

    vec3 ro = camera_position;

    vec3 rd;
    float d;
    gen_ray(scaled_depth, uv, rd, d);

    vec4 shaded_color = ray_march(ro, rd, d);

    p3d_FragColor = blend_onto(shaded_color, scene_color);
}
