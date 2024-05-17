// Port of the geometry shader example from https://github.com/mhalber/Lines

#version 330

uniform vec2 aa_radius;
      
in vec4 g_col;
noperspective in float g_u;
noperspective in float g_v;
noperspective in float g_line_width;
noperspective in float g_line_length;

out vec4 p3d_FragColor;

void main() {
    /* We render a quad that is fattened by r, giving total width of the line to be w+r. We want smoothing to happen
        around w, so that the edge is properly smoothed out. As such, in the smoothstep function we have:
        Far edge   : 1.0                                          = (w+r) / (w+r)
        Close edge : 1.0 - (2r / (w+r)) = (w+r)/(w+r) - 2r/(w+r)) = (w-r) / (w+r)
        This way the smoothing is centered around 'w'.
        */
    float au = 1.0 - smoothstep( 1.0 - ((2.0*aa_radius[0]) / g_line_width),  1.0, abs(g_u / g_line_width) );
    float av = 1.0 - smoothstep( 1.0 - ((2.0*aa_radius[1]) / g_line_length), 1.0, abs(g_v / g_line_length) );
    p3d_FragColor = g_col;
    p3d_FragColor.a *= min(av, au);
}