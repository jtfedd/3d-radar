$begin constants
#define PI 3.1415926538
$end

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
    return texelFetch(volume_data, offset[sweep_index] + buff_index).x;
}

float data_value(vec3 point) {
    float el = atan(point.z, length(point.xy));
    if (el <= elevation[0] || el >= elevation[scan_count[0] - 1]) {
        return -1.0;
    }

    int sweep_index = calc_sweep_index(el);

    return data_value_for_sweep(point, sweep_index);
}