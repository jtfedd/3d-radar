// https://www.shadertoy.com/view/4djSRW
// float hash12(vec2 p) {
// 	vec3 p3  = fract(vec3(p.xyx) * .1031);
//     p3 += dot(p3, p3.yzx + 33.33);
//     return fract((p3.x + p3.y) * p3.z);
// }

float hash13(vec3 p3) {
	p3  = fract(p3 * .1031);
    p3 += dot(p3, p3.zyx + 31.32);
    return fract((p3.x + p3.y) * p3.z);
}

float hash14(vec4 p4) {
	p4 = fract(p4  * vec4(.1031, .1030, .0973, .1099));
    p4 += dot(p4, p4.wzxy+33.33);
    return fract((p4.x + p4.y) * (p4.z + p4.w));
}