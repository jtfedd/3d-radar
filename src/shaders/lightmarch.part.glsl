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