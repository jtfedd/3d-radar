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