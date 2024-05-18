#version 150

uniform float	thickness;		// the thickness of the line in pixels
uniform float	miter_limit;	// 1.0: always miter, -1.0: never miter, 0.75: default
uniform vec2	window_size;	// the size of the viewport in pixels

layout( lines_adjacency ) in;
layout( triangle_strip, max_vertices = 7 ) out;

in vec4 v_color[4];

out vec4 g_color;

vec2 toScreenSpace( vec4 vertex ) {
	return vec2( vertex.xy / vertex.w ) * window_size;
}

void main( void ) {
	// get the four vertices passed to the shader:
	vec2 p0 = toScreenSpace( gl_in[0].gl_Position );	// start of previous segment
	vec2 p1 = toScreenSpace( gl_in[1].gl_Position );	// end of previous segment, start of current segment
	vec2 p2 = toScreenSpace( gl_in[2].gl_Position );	// end of current segment, start of next segment
	vec2 p3 = toScreenSpace( gl_in[3].gl_Position );	// end of next segment

	// perform naive culling
	// vec2 area = window_size * 1.2;
	// if( p1.x < -area.x || p1.x > area.x ) return;
	// if( p1.y < -area.y || p1.y > area.y ) return;
	// if( p2.x < -area.x || p2.x > area.x ) return;
	// if( p2.y < -area.y || p2.y > area.y ) return;

	// determine the direction of each of the 3 segments (previous, current, next)
	vec2 v0 = normalize( p1 - p0 );
	vec2 v1 = normalize( p2 - p1 );
	vec2 v2 = normalize( p3 - p2 );

	// determine the normal of each of the 3 segments (previous, current, next)
	vec2 n0 = vec2( -v0.y, v0.x );
	vec2 n1 = vec2( -v1.y, v1.x );
	vec2 n2 = vec2( -v2.y, v2.x );

	// determine miter lines by averaging the normals of the 2 segments
	vec2 miter_a = normalize( n0 + n1 );	// miter at start of current segment
	vec2 miter_b = normalize( n1 + n2 );	// miter at end of current segment

	// determine the length of the miter by projecting it onto normal and then inverse it
	float length_a = thickness / dot( miter_a, n1 );
	float length_b = thickness / dot( miter_b, n1 );

	// prevent excessively long miters at sharp corners
	if( dot( v0, v1 ) < -miter_limit ) {
		miter_a = n1;
		length_a = thickness;

		// close the gap
		if( dot( v0, n1 ) > 0 ) {
			g_color = v_color[1];
			gl_Position = vec4( ( p1 + thickness * n0 ) / window_size, 0.0, 1.0 );
			EmitVertex();

			g_color = v_color[1];
			gl_Position = vec4( ( p1 + thickness * n1 ) / window_size, 0.0, 1.0 );
			EmitVertex();

			g_color = v_color[1];
			gl_Position = vec4( p1 / window_size, 0.0, 1.0 );
			EmitVertex();

			EndPrimitive();
		} else {
			g_color = v_color[1];
			gl_Position = vec4( ( p1 - thickness * n1 ) / window_size, 0.0, 1.0 );
			EmitVertex();

			g_color = v_color[1];
			gl_Position = vec4( ( p1 - thickness * n0 ) / window_size, 0.0, 1.0 );
			EmitVertex();

			g_color = v_color[1];
			gl_Position = vec4( p1 / window_size, 0.0, 1.0 );
			EmitVertex();

			EndPrimitive();
		}
	}

	if ( dot( v1, v2 ) < -miter_limit ) {
		miter_b = n1;
		length_b = thickness;
	}

	// generate the triangle strip
	g_color = v_color[1];
	gl_Position = vec4( ( p1 + length_a * miter_a ) / window_size, 0.0, 1.0 );
	EmitVertex();

	g_color = v_color[1];
	gl_Position = vec4( ( p1 - length_a * miter_a ) / window_size, 0.0, 1.0 );
	EmitVertex();

	g_color = v_color[2];
	gl_Position = vec4( ( p2 + length_b * miter_b ) / window_size, 0.0, 1.0 );
	EmitVertex();

	g_color = v_color[2];
	gl_Position = vec4( ( p2 - length_b * miter_b ) / window_size, 0.0, 1.0 );
	EmitVertex();

	EndPrimitive();
}