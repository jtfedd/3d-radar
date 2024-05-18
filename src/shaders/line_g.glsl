#version 330

layout(lines) in;
layout(triangle_strip, max_vertices = 4) out;

uniform vec2 window_size;
uniform float thickness;

in vec4 vertex_color[];
out vec4 geometry_color;

void main() {
    float u_width        = window_size[0];
    float u_height       = window_size[1];
    float u_aspect_ratio = u_height / u_width;

    vec2 ndc_a = gl_in[0].gl_Position.xy / gl_in[0].gl_Position.w;
    vec2 ndc_b = gl_in[1].gl_Position.xy / gl_in[1].gl_Position.w;

    vec2 line_vector = ndc_b - ndc_a;
    vec2 dir = normalize(vec2( line_vector.x, line_vector.y * u_aspect_ratio ));

    vec2 normal    = vec2( -dir.y, dir.x );
    vec2 normal_a  = vec2( thickness/u_width, thickness/u_height ) * normal;
    vec2 normal_b  = vec2( thickness/u_width, thickness/u_height ) * normal;

    // Start point
    geometry_color = vertex_color[0];

    gl_Position = vec4( (ndc_a + normal_a) * gl_in[0].gl_Position.w, gl_in[0].gl_Position.zw );
    EmitVertex();

    gl_Position = vec4( (ndc_a - normal_a) * gl_in[0].gl_Position.w, gl_in[0].gl_Position.zw );
    EmitVertex();

    // End point
    geometry_color = vertex_color[1];

    gl_Position = vec4( (ndc_b + normal_b) * gl_in[1].gl_Position.w, gl_in[1].gl_Position.zw );
    EmitVertex();

    gl_Position = vec4( (ndc_b - normal_b) * gl_in[1].gl_Position.w, gl_in[1].gl_Position.zw );
    EmitVertex();

    EndPrimitive();
}