float interpolate(float low, float high, float factor) {
    if (low < 0 && high < 0) {
        return -1;
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