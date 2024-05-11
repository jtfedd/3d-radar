#version 330

#define MAX_SCANS 20

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
uniform sampler2D color_scale;

uniform float ambient_intensity;
uniform float directional_intensity;
uniform vec3 directional_orientation;
uniform bool volumetric_lighting;

// End inputs

#define PI 3.1415926538

#define MIN_STEPS 5
#define MAX_STEPS 1000
#define STEP_SIZE 1.5

#define MIN_L_STEPS 5
#define MAX_L_STEPS 20
#define L_STEP_SIZE 1.5

#define ALPHA_CUTOFF 0.99

// ########## start #include hash.part.glsl

// https://www.shadertoy.com/view/4djSRW
// float hash12(vec2 p) {
// 	vec3 p3  = fract(vec3(p.xyx) * .1031);
//     p3 += dot(p3, p3.yzx + 33.33);
//     return fract((p3.x + p3.y) * p3.z);
// }

float hash13(vec3 p3) {
	p3  = fract(p3 * .1031);
    p3 += dot(p3, p3.zyx + 31.32);
    return fract((p3.x + p3.y) * p3.z);
}

float hash14(vec4 p4) {
	p4 = fract(p4  * vec4(.1031, .1030, .0973, .1099));
    p4 += dot(p4, p4.wzxy+33.33);
    return fract((p4.x + p4.y) * (p4.z + p4.w));
}
// ########## end #include hash.part.glsl
// ########## start #include box_intersection.part.glsl

// For each coord, return the range of t for which p+t*v is inside the box defined
// by the corners box_min and box_max, and whether the ray intersects the box.
// More on this method here: https://tavianator.com/2011/ray_box.html
void box_intersection(
    in vec3 box_min, in vec3 box_max,
    in vec3 p, in vec3 v,
    out vec2 tRange, out bool no_intersection
) {
    vec3 tb0 = (box_min - p) / v;
    vec3 tb1 = (box_max - p) / v;
    vec3 tmin = min(tb0, tb1);
    vec3 tmax = max(tb0, tb1);

    tRange = vec2(
        max(max(tmin.x, tmin.y), tmin.z),
        min(min(tmax.x, tmax.y), tmax.z)
    );

    no_intersection = tRange.t < tRange.s;
}
// ########## end #include box_intersection.part.glsl
// ########## start #include color_util.part.glsl

vec4 blend_onto(vec4 front, vec4 behind) {
    return front + (1.0 - front.a) * behind;
}

vec3 colorize(float value) {
    return texture(color_scale, vec2(0, value)).rgb;
}
// ########## end #include color_util.part.glsl
// ########## start #include density.part.glsl

float density(float value) {
    if (value < 0) return 0.0;

    value = abs((value + density_params[0]) * density_params[1]);

    // Apply low and high cutoff
    if (value <= density_params[5]) return density_params[2];
    if (value >= density_params[6]) return density_params[3];

    value = (value - density_params[5]) / (density_params[6] - density_params[5]);
    return density_params[2] + density_params[3] * pow(value, density_params[4]);
}
// ########## end #include density.part.glsl
// ########## start #include resolve_elevation.part.glsl

int calc_sweep_index(float el) {
    int l = 0;
    int r = scan_count[0];

    for (int i = 0; i < 20; i++) {
        int m = (l + r) / 2;

        if (el < elevation[m]) {
            r = m;
        } else {
            l = m;
        }

        if (r - l <= 1) {
            return l;
        }
    }

    return 0;
}

// ########## end #include resolve_elevation.part.glsl
// ########## start #include volume_smooth.part.glsl

float interpolate(float low, float high, float factor) {
    if (low < 0 && high < 0) {
        return -1.0;
    }

    if (low < 0) {
        low = -density_params[0];
    }

    if (high < 0) {
        high = -density_params[0];
    }

    return (low * (1 - factor)) + (high * factor);
}

float data_value_for_indices(int sweep_index, int az_index, int r_index) {
    int buff_index = r_count[sweep_index] * az_index + r_index;
    return texelFetch(volume_data, offset[sweep_index] + buff_index).x;
}

float data_value_for_gate(vec3 point, int sweep_index, int r_index) {
    if (az_count[sweep_index] == 0) {
        return -1.0;
    }

    float az = mod(atan(point.x, point.y) - (az_step[sweep_index] / 2), PI*2);
    int az_index = int(floor(az / az_step[sweep_index]));
    if (az_index < 0) {
        return -1.0;
    }

    int az_next = az_index + 1;
    if (az_next == az_count[sweep_index]) {
        az_next = 0;
    }

    float factor = (az - (az_index * az_step[sweep_index])) / (((az_index + 1) * az_step[sweep_index]) - (az_index * az_step[sweep_index]));
    float low = data_value_for_indices(sweep_index, az_index, r_index);
    float high = data_value_for_indices(sweep_index, az_next, r_index);

    return interpolate(low, high, factor);
}

float data_value_for_sweep(vec3 point, int sweep_index) {
    if (r_count[sweep_index] == 0) {
        return -1.0;
    }

    float r = length(point);
    int r_index = int(floor((r - r_first[sweep_index]) / r_step[sweep_index]));
    if (r_index < 0 || r_index >= r_count[sweep_index]) {
        return -1.0;
    }

    float low = data_value_for_gate(point, sweep_index, r_index);
    float high = data_value_for_gate(point, sweep_index, r_index + 1);
    float prev = r_first[sweep_index] + (r_step[sweep_index] * r_index);
    float factor = (r - prev) / (r_step[sweep_index]);
    return interpolate(low, high, factor);
}

float data_value(vec3 point) {
    float el = atan(point.z, length(point.xy));
    if (el <= elevation[0] || el >= elevation[scan_count[0] - 1]) {
        return -1.0;
    }

    int sweep_index = calc_sweep_index(el);

    float low = data_value_for_sweep(point, sweep_index);
    float high = data_value_for_sweep(point, sweep_index+1);

    float factor = (el - elevation[sweep_index]) / (elevation[sweep_index+1] - elevation[sweep_index]);
    return interpolate(low, high, factor);
}
// ########## end #include volume_smooth.part.glsl
// ########## start #include lightmarch.part.glsl

float light_amount(in vec3 ro) {
    vec3 rd = -directional_orientation;

    vec2 tRange;
    bool no_intersection;
    box_intersection(bounds_start, bounds_end, ro, rd, tRange, no_intersection);

    if (no_intersection) {
        return 1.0;
    }

    // Make sure the range starts at the origin
    tRange.s = max(0.0, tRange.s);

    float step_size = min(L_STEP_SIZE, (tRange.t - tRange.s) / MIN_L_STEPS);
    float jitter = min(tRange.t - tRange.s, step_size)*hash14(vec4(ro.xyz, time));
    float t = tRange.s + jitter;

    float opacity = 0.0;
    for (int i = 0; i < MAX_L_STEPS; i++) {
        if (t > tRange.t || (opacity > ALPHA_CUTOFF)) {
            break;
        }

        vec3 sample_pos = ro + t * rd;

        float sample_value = data_value(sample_pos);
        float sample_density = density(sample_value);
        float sample_opacity = sample_density * step_size;

        opacity = sample_opacity + (1.0 - sample_opacity) * opacity;
        
        t += step_size;
    }

    if (opacity > ALPHA_CUTOFF) {
        return 0.0;
    }

    return 1 - opacity;
}
// ########## end #include lightmarch.part.glsl
// ########## start #include raymarch.part.glsl

void gen_ray(
    in float depth_clip, in vec2 uv,
    out vec3 ray, out float d
) {    
    vec4 ray_clip = vec4(uv, depth_clip, 1.0);
    vec4 ray_eye = (projection_matrix_inverse * ray_clip);
    ray_eye /= ray_eye.w;
    d = length(ray_eye.xyz);

    ray_eye = vec4(ray_eye.xyz, 0.0);

    vec3 ray_world = (inverse(trans_world_to_model_of_camera) * ray_eye).xyz;
    ray = normalize(ray_world);
}

// Ray marching loop based on https://www.shadertoy.com/view/tdjBR1
vec4 ray_march(in vec3 ro, in vec3 rd, in float d) {
    vec2 tRange;
    bool no_intersection;
    box_intersection(bounds_start, bounds_end, ro, rd, tRange, no_intersection);

    vec4 color = vec4(0.0);
    if (no_intersection) {
        return color;
    }

    // Make sure the range does not start behind the camera
    tRange.s = max(0.0, tRange.s);
    
    // Don't cast the ray further than the first rendered object
    tRange.t = min(d, tRange.t);

    // Use a smaller step size when the slice of volume is very thin
    float step_size = min(STEP_SIZE, (tRange.t - tRange.s) / MIN_STEPS);

    float jitter = min(tRange.t-tRange.s, step_size)*hash13(vec3(gl_FragCoord.xy, time));
    float t = tRange.s + jitter;

    for (int i = 0; i < MAX_STEPS; i++) {
        // If we have moved out of the bounding box, or sufficiently opaque, exit the loop
        if (t > tRange.t || color.a > ALPHA_CUTOFF) {
            break;
        }

        vec3 sample_pos = ro + t * rd;

        float sample_value = data_value(sample_pos);
        float sample_density = density(sample_value);
        vec3 sample_color = colorize(sample_value);
        float sample_alpha = sample_density * step_size;

        float brightness = volumetric_lighting
            ? (sample_alpha < (1 - ALPHA_CUTOFF) ? 1.0 : light_amount(sample_pos))
            : 1.0;
        float lighting = volumetric_lighting
            ? ambient_intensity + ((1 - ambient_intensity) * (brightness * directional_intensity))
            : 1.0;

        vec4 ci = vec4(sample_color * lighting, 1.0) * sample_alpha;
        color = blend_onto(color, ci);

        t += step_size;
    }

    if (color.a > ALPHA_CUTOFF) {
        color.a = 1.0;
    }
    
    return color;
}
// ########## end #include raymarch.part.glsl

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
