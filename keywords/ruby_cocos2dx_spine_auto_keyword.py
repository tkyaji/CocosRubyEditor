def get_keywords():
	return {'classes': {'SP::SkeletonAnimation': {'base_class': 'SP::SkeletonRenderer', 'ifunctions': {'set_mix(from_animation, to_animation, duration)': {'ret_type': 'void', 'arguments': [{'type': 'string', 'name': 'from_animation'}, {'type': 'string', 'name': 'to_animation'}, {'type': 'float', 'name': 'duration'}], 'sublime': 'set_mix(${1:from_animation}, ${2:to_animation}, ${3:duration})$0'}, 'clear_track()': {'ret_type': 'void', 'arguments': [], 'sublime': 'clear_track'}, 'set_track_start_listener(entry, listener)': {'ret_type': 'void', 'arguments': [{'type': 'spTrackEntry', 'name': 'entry'}, {'type': 'Proc', 'name': 'listener'}], 'sublime': 'set_track_start_listener(${1:entry}, ${2:listener})$0'}, 'set_event_listener(listener)': {'ret_type': 'void', 'arguments': [{'type': 'Proc', 'name': 'listener'}], 'sublime': 'set_event_listener(${1:listener})$0'}, 'set_complete_listener(listener)': {'ret_type': 'void', 'arguments': [{'type': 'Proc', 'name': 'listener'}], 'sublime': 'set_complete_listener(${1:listener})$0'}, 'set_end_listener(listener)': {'ret_type': 'void', 'arguments': [{'type': 'Proc', 'name': 'listener'}], 'sublime': 'set_end_listener(${1:listener})$0'}, 'set_track_event_listener(entry, listener)': {'ret_type': 'void', 'arguments': [{'type': 'spTrackEntry', 'name': 'entry'}, {'type': 'Proc', 'name': 'listener'}], 'sublime': 'set_track_event_listener(${1:entry}, ${2:listener})$0'}, 'clear_track(track_index)': {'ret_type': 'void', 'arguments': [{'type': 'int', 'name': 'track_index'}], 'sublime': 'clear_track(${1:track_index})$0'}, 'set_start_listener(listener)': {'ret_type': 'void', 'arguments': [{'type': 'Proc', 'name': 'listener'}], 'sublime': 'set_start_listener(${1:listener})$0'}, 'clear_tracks()': {'ret_type': 'void', 'arguments': [], 'sublime': 'clear_tracks'}, 'set_track_end_listener(entry, listener)': {'ret_type': 'void', 'arguments': [{'type': 'spTrackEntry', 'name': 'entry'}, {'type': 'Proc', 'name': 'listener'}], 'sublime': 'set_track_end_listener(${1:entry}, ${2:listener})$0'}, 'set_track_complete_listener(entry, listener)': {'ret_type': 'void', 'arguments': [{'type': 'spTrackEntry', 'name': 'entry'}, {'type': 'Proc', 'name': 'listener'}], 'sublime': 'set_track_complete_listener(${1:entry}, ${2:listener})$0'}}, 'sfunctions': {}}, 'SP::SkeletonRenderer': {'base_class': 'CC::Node', 'ifunctions': {'set_debug_bones_enabled(enabled)': {'ret_type': 'void', 'arguments': [{'type': 'bool', 'name': 'enabled'}], 'sublime': 'set_debug_bones_enabled(${1:enabled})$0'}, 'set_time_scale(scale)': {'ret_type': 'void', 'arguments': [{'type': 'float', 'name': 'scale'}], 'sublime': 'set_time_scale(${1:scale})$0'}, 'set_to_setup_pose()': {'ret_type': 'void', 'arguments': [], 'sublime': 'set_to_setup_pose'}, 'get_skeleton()': {'ret_type': 'spSkeleton', 'arguments': [], 'sublime': 'get_skeleton'}, 'get_debug_bones_enabled()': {'ret_type': 'bool', 'arguments': [], 'sublime': 'get_debug_bones_enabled'}, 'set_skin(skin_name)': {'ret_type': 'bool', 'arguments': [{'type': 'string', 'name': 'skin_name'}], 'sublime': 'set_skin(${1:skin_name})$0'}, 'get_debug_slots_enabled()': {'ret_type': 'bool', 'arguments': [], 'sublime': 'get_debug_slots_enabled'}, 'set_slots_to_setup_pose()': {'ret_type': 'void', 'arguments': [], 'sublime': 'set_slots_to_setup_pose'}, 'set_bones_to_setup_pose()': {'ret_type': 'void', 'arguments': [], 'sublime': 'set_bones_to_setup_pose'}, 'set_opacity_modify_rgb(value)': {'ret_type': 'void', 'arguments': [{'type': 'bool', 'name': 'value'}], 'sublime': 'set_opacity_modify_rgb(${1:value})$0'}, 'set_debug_slots_enabled(enabled)': {'ret_type': 'void', 'arguments': [{'type': 'bool', 'name': 'enabled'}], 'sublime': 'set_debug_slots_enabled(${1:enabled})$0'}, 'opacity_modify_rgb?()': {'ret_type': 'bool', 'arguments': [], 'sublime': 'opacity_modify_rgb?'}, 'get_time_scale()': {'ret_type': 'float', 'arguments': [], 'sublime': 'get_time_scale'}}, 'sfunctions': {'create_with_file(skeleton_data_file, atlas)': {'ret_type': 'SP::SkeletonRenderer', 'arguments': [{'type': 'string', 'name': 'skeleton_data_file'}, {'type': 'spAtlas', 'name': 'atlas'}], 'sublime': 'create_with_file(${1:skeleton_data_file}, ${2:atlas})$0'}, 'create_with_file(skeleton_data_file, atlas_file, scale)': {'ret_type': 'SP::SkeletonRenderer', 'arguments': [{'type': 'string', 'name': 'skeleton_data_file'}, {'type': 'string', 'name': 'atlas_file'}, {'type': 'float', 'name': 'scale'}], 'sublime': 'create_with_file(${1:skeleton_data_file}, ${2:atlas_file}, ${3:scale})$0'}, 'create_with_file(skeleton_data_file, atlas_file)': {'ret_type': 'SP::SkeletonRenderer', 'arguments': [{'type': 'string', 'name': 'skeleton_data_file'}, {'type': 'string', 'name': 'atlas_file'}], 'sublime': 'create_with_file(${1:skeleton_data_file}, ${2:atlas_file})$0'}, 'create_with_file(skeleton_data_file, atlas, scale)': {'ret_type': 'SP::SkeletonRenderer', 'arguments': [{'type': 'string', 'name': 'skeleton_data_file'}, {'type': 'spAtlas', 'name': 'atlas'}, {'type': 'float', 'name': 'scale'}], 'sublime': 'create_with_file(${1:skeleton_data_file}, ${2:atlas}, ${3:scale})$0'}}}}, 'tree': {'SP': {'SkeletonRenderer': 'SP::SkeletonRenderer', 'SkeletonAnimation': 'SP::SkeletonAnimation'}}}
