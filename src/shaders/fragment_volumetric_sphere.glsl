#version 460

// Inputs from program
uniform vec2 resolution;
uniform vec3 camera_position;

uniform vec3 bounds_start;
uniform vec3 bounds_end;

uniform sampler2D scene;
uniform sampler2D depth;

uniform mat4 trans_world_to_model_of_camera;
uniform mat4 projection_matrix_inverse;

uniform float time;

// Outputs to Panda3D
out vec4 p3d_FragColor;

const float MIN_STEPS = 5;
const float MAX_STEPS = 1000;
const float STEP_SIZE = 0.1;
const float ALPHA_CUTOFF = 0.99;

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

float density(in vec3 point, in vec3 center, float radius) {
    if (length(point - center) < radius) {
        return 2 - 2 * pow((length(point - center) / radius), 3.0f);
    }

    return 0.0;
}

vec4 blend_onto(vec4 front, vec4 behind) {
    return front + (1.0 - front.a) * behind;
}

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

// https://www.shadertoy.com/view/4djSRW
float hash12(vec2 p) {
	vec3 p3  = fract(vec3(p.xyx) * .1031);
    p3 += dot(p3, p3.yzx + 33.33);
    return fract((p3.x + p3.y) * p3.z);
}

float hash13(vec3 p3) {
	p3  = fract(p3 * .1031);
    p3 += dot(p3, p3.zyx + 31.32);
    return fract((p3.x + p3.y) * p3.z);
}

vec4 ray_march(in vec3 ro, in vec3 rd, in float d) {
    vec2 tRange;
    bool no_intersection;
    box_intersection(bounds_start, bounds_end, ro, rd, tRange, no_intersection);

    // Make sure the range does not start behind the camera
    tRange.s = max(0.0, tRange.s);
    
    // Don't cast the ray further than the first rendered object
    tRange.t = min(d, tRange.t);

    vec4 color = vec4(0.0);

    if (no_intersection) {
        return color;
    }

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

        float sample_density = density(sample_pos, vec3(0.0, 0.0, 0.0), 2.0);
        float sample_attenuation = exp(-step_size * sample_density);
        vec3 sample_color = vec3(1.0 - sample_density, 0, sample_density);
        float sample_alpha = sample_density * step_size;

        vec4 ci = vec4(sample_color, 1.0) * sample_alpha;
        color = blend_onto(color, ci);

        t += step_size;
    }

    if (color.a > ALPHA_CUTOFF) {
        color.a = 1.0;
    }
    
    return color;
}

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