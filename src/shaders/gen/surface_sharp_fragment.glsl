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

uniform usamplerBuffer volume_data;

uniform sampler2D color_scale;

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


float data_value_for_sweep(vec3 point, int sweep_index) {
    if (r_count[sweep_index] == 0) {
        return -1.0;
    }

    float r = length(point);
    int r_index = int(floor((r - r_first[sweep_index]) / r_step[sweep_index]));
    if (r_index < 0 || r_index >= r_count[sweep_index]) {
        return -1.0;
    }

    if (az_count[sweep_index] == 0) {
        return -1.0;
    }

    float az = mod(atan(point.x, point.y), PI*2);
    int az_index = int(floor(az / az_step[sweep_index]));
    if (az_index < 0) {
        return -1.0;
    }

    int buff_index = r_count[sweep_index] * az_index + r_index;
    int value = int(texelFetch(volume_data, offset[sweep_index] + buff_index).x);
    if (value == 0.0) {
        return -1.0;
    }
    return float(value - 1) / 254.0;
}

float data_value(vec3 point) {
    float el = atan(point.z, length(point.xy));
    if (el <= elevation[0] || el >= elevation[scan_count[0] - 1]) {
        return -1.0;
    }

    int sweep_index = calc_sweep_index(el);

    return data_value_for_sweep(point, sweep_index);
}

vec4 blend_onto(vec4 front, vec4 behind) {
    return front + (1.0 - front.a) * behind;
}

vec3 colorize(float value) {
    return texture(color_scale, vec2(0, value)).rgb;
}

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