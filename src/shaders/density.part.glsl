float density(float value) {
    if (value < 0) return 0;

    value = abs((value + density_params[0]) * density_params[1]);
    return density_params[2] + density_params[3] * pow(value, density_params[4]);
}

// Hello