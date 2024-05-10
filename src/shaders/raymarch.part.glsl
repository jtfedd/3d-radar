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

        float brightness = sample_alpha < (1 - ALPHA_CUTOFF) ? 1.0 : light_amount(sample_pos);
        brightness = ambient_intensity + ((1 - ambient_intensity) * (brightness * directional_intensity));

        vec4 ci = vec4(sample_color * brightness, 1.0) * sample_alpha;
        color = blend_onto(color, ci);

        t += step_size;
    }

    if (color.a > ALPHA_CUTOFF) {
        color.a = 1.0;
    }
    
    return color;
}