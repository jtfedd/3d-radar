$begin inputs
uniform sampler2D color_scale;
$end

vec4 blend_onto(vec4 front, vec4 behind) {
    return front + (1.0 - front.a) * behind;
}

vec3 colorize(float value) {
    return texture(color_scale, vec2(0, value)).rgb;
}