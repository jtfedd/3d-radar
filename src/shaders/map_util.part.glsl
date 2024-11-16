$begin inputs
uniform vec3 world_pos;
uniform vec3 camera_pos;
$end

bool backface(vec3 pos) {
    return dot((pos - camera_pos), (pos - world_pos)) > 0;
}