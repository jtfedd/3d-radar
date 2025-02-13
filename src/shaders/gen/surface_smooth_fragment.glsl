#version 330

#define MAX_SCANS 20
#define PI 3.1415926538

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

uniform sampler2D color_scale;

// World-space vertex position from vertex shader
in vec3 vpos;

// Outputs to Panda3D
out vec4 p3d_FragColor;

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

vec3 resolve_surface_sample_position(vec3 surface_pos, int sweep_index) {
    vec3 ray = surface_pos - earth_center;
    vec3 up = -earth_center;
    float center_angle = acos(dot(ray, up)/ (length(ray) * length(up)));
    float x_angle = (PI / 2.0) + elevation[sweep_index];
    float a_angle = PI - x_angle - center_angle;
    float a = length(up);
    float x = (a / sin(a_angle)) * sin(x_angle);
    vec3 sample_pos = earth_center + (normalize(ray)*x);
    return sample_pos;
}

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
    int value = int(texelFetch(volume_data, offset[sweep_index] + buff_index).x);
    if (value == 0.0) {
        return -1.0;
    }
    return (value - 1.0) / 254.0;
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

vec4 blend_onto(vec4 front, vec4 behind) {
    return front + (1.0 - front.a) * behind;
}

vec3 colorize(float value) {
    return texture(color_scale, vec2(0, value)).rgb;
}
vec3 resolve_surface_color() {
    if (scan_count[0] < 3) discard;

    bool hasValue = false;
    float value = -1;
    float maxIntensity = -1;

    for (int i = 1; i < MAX_SCANS; i++) {
        if (i > max_el_index || i >= scan_count[0]) break;

        vec3 sample_pos = resolve_surface_sample_position(vpos, i);
        float sample_value = data_value_for_sweep(sample_pos, i);
        float intensity = abs((sample_value + density_params[0]) * density_params[1]);
        if (sample_value < 0 || intensity < threshold) continue;

        hasValue = true;
        if (intensity > maxIntensity) {
            value = sample_value;
            maxIntensity = intensity;
        }
    }

    if (!hasValue) discard;
    
    return colorize(value);
}
      
void main() {
    vec3 color = resolve_surface_color();
    p3d_FragColor = vec4(color.xyz, opacity);
}