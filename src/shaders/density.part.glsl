float density(float value) {
    if (value < 0) return 0.0;

    value = abs((value + density_params[0]) * density_params[1]);

    // Apply low and high cutoff
    value = max(value, density_params[5]);
    value = min(value, density_params[6]);

    value = (value - density_params[5]) / (density_params[6] - density_params[5]);
    return density_params[2] + density_params[3] * pow(value, density_params[4]);
}