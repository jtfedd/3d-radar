// Port of the geometry shader example from https://github.com/mhalber/Lines

#version 330

layout(lines) in;
layout(triangle_strip, max_vertices = 4) out;

uniform vec2 viewport_size;
uniform vec2 aa_radius;
uniform float line_width;

in vec4 vertex_color[];

out vec4 g_col;
noperspective out float g_line_width;
noperspective out float g_line_length;
noperspective out float g_u;
noperspective out float g_v;

void main() {
    float u_width        = viewport_size[0];
    float u_height       = viewport_size[1];
    float u_aspect_ratio = u_height / u_width;

    vec2 ndc_a = gl_in[0].gl_Position.xy / gl_in[0].gl_Position.w;
    vec2 ndc_b = gl_in[1].gl_Position.xy / gl_in[1].gl_Position.w;

    vec2 line_vector = ndc_b - ndc_a;
    vec2 viewport_line_vector = line_vector * viewport_size;
    vec2 dir = normalize(vec2( line_vector.x, line_vector.y * u_aspect_ratio ));

    float line_width_a     = max( 1.0, line_width ) + aa_radius[0];
    float line_width_b     = max( 1.0, line_width ) + aa_radius[0];
    float extension_length = aa_radius[1];
    float line_length      = length( viewport_line_vector ) + 2.0 * extension_length;

    vec2 normal    = vec2( -dir.y, dir.x );
    vec2 normal_a  = vec2( line_width_a/u_width, line_width_a/u_height ) * normal;
    vec2 normal_b  = vec2( line_width_b/u_width, line_width_b/u_height ) * normal;
    vec2 extension = vec2( extension_length / u_width, extension_length / u_height ) * dir;

    g_col = vec4( vertex_color[0].rgb, vertex_color[0].a * min( line_width, 1.0f ) );
    g_u = line_width_a;
    g_v = line_length * 0.5;
    g_line_width = line_width_a;
    g_line_length = line_length * 0.5;
    gl_Position = vec4( (ndc_a + normal_a - extension) * gl_in[0].gl_Position.w, gl_in[0].gl_Position.zw );
    EmitVertex();

    g_u = -line_width_a;
    g_v = line_length * 0.5;
    g_line_width = line_width_a;
    g_line_length = line_length * 0.5;
    gl_Position = vec4( (ndc_a - normal_a - extension) * gl_in[0].gl_Position.w, gl_in[0].gl_Position.zw );
    EmitVertex();

    g_col = vec4( vertex_color[1].rgb, vertex_color[1].a * min( line_width, 1.0f ) );
    g_u = line_width_b;
    g_v = -line_length * 0.5;
    g_line_width = line_width_b;
    g_line_length = line_length * 0.5;
    gl_Position = vec4( (ndc_b + normal_b + extension) * gl_in[1].gl_Position.w, gl_in[1].gl_Position.zw );
    EmitVertex();

    g_u = -line_width_b;
    g_v = -line_length * 0.5;
    g_line_width = line_width_b;
    g_line_length = line_length * 0.5;
    gl_Position = vec4( (ndc_b - normal_b + extension) * gl_in[1].gl_Position.w, gl_in[1].gl_Position.zw );
    EmitVertex();

    EndPrimitive();
}