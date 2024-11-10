#version 330

uniform vec2 window_size;
uniform float thickness;

$inputs

layout(lines_adjacency) in;
layout(triangle_strip, max_vertices = 7) out;

in vec3 vpos[4];

out vec3 gpos;

#include map_util.part.glsl

void main() {
    // Cull segments below the clip plane
    if (backface(vpos[1]) && backface(vpos[2])) {
        return;
    }

    float u_width        = window_size[0];
    float u_height       = window_size[1];
    float u_aspect_ratio = u_height / u_width;

    // ndc_ctl references the control point before the current segment
    // This is used to generate a triangle to bridge the segment with the previous
    vec2 ndc_ctl = gl_in[0].gl_Position.xy / gl_in[0].gl_Position.w;
    vec2 ndc_a = gl_in[1].gl_Position.xy / gl_in[1].gl_Position.w;
    vec2 ndc_b = gl_in[2].gl_Position.xy / gl_in[2].gl_Position.w;

    vec2 line_vector = ndc_b - ndc_a;
    vec2 dir = normalize(vec2( line_vector.x, line_vector.y * u_aspect_ratio ));

    vec2 ctl_vector = ndc_a - ndc_ctl;
    vec2 ctl_dir = normalize(vec2( ctl_vector.x, ctl_vector.y * u_aspect_ratio ));

    // vec2( -dir.y, dir.x ) is the normal vector
    // vec2( thicknes/u_width, thickness/u_height ) scales it by the thickness of the line
    vec2 normal  = vec2( thickness/u_width, thickness/u_height ) * vec2( -dir.y, dir.x );

    vec2 ctl_normal = vec2( thickness/u_width, thickness/u_height ) * vec2( -ctl_dir.y, ctl_dir.x );

    // Generate a triangle to bridge this segment with the previous
    gpos = vpos[1];

    gl_Position = gl_in[1].gl_Position;
    EmitVertex();

    if ( dot( ctl_normal, dir ) > 0 ) {
        // Left turn
        gl_Position = vec4( (ndc_a - ctl_normal) * gl_in[1].gl_Position.w, gl_in[1].gl_Position.zw);
        EmitVertex();

        gl_Position = vec4( (ndc_a - normal) * gl_in[1].gl_Position.w, gl_in[1].gl_Position.zw);
        EmitVertex();
    } else {
        // Right turn
        gl_Position = vec4( (ndc_a + normal) * gl_in[1].gl_Position.w, gl_in[1].gl_Position.zw);
        EmitVertex();

        gl_Position = vec4( (ndc_a + ctl_normal) * gl_in[1].gl_Position.w, gl_in[1].gl_Position.zw);
        EmitVertex();
    }

    EndPrimitive();

    // Generate the segment
    gl_Position = vec4( (ndc_a + normal) * gl_in[1].gl_Position.w, gl_in[1].gl_Position.zw );
    EmitVertex();

    gl_Position = vec4( (ndc_a - normal) * gl_in[1].gl_Position.w, gl_in[1].gl_Position.zw );
    EmitVertex();

    gpos = vpos[2];
    
    gl_Position = vec4( (ndc_b + normal) * gl_in[2].gl_Position.w, gl_in[2].gl_Position.zw );
    EmitVertex();

    gl_Position = vec4( (ndc_b - normal) * gl_in[2].gl_Position.w, gl_in[2].gl_Position.zw );
    EmitVertex();

    EndPrimitive();
}