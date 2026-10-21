extends Node3D

# Keep the starter kit's existing animation interface.
func _ready() -> void:
	var imported_player := $Portrait.find_child("AnimationPlayer", true, false) as AnimationPlayer
	if imported_player == null:
		push_error("Portrait model is missing its AnimationPlayer")
		return
	imported_player.get_parent().remove_child(imported_player)
	imported_player.name = "AnimationPlayer"
	add_child(imported_player)
	imported_player.root_node = NodePath("../Portrait")
	for library_name in imported_player.get_animation_library_list():
		var library := imported_player.get_animation_library(library_name)
		for animation_name in library.get_animation_list():
			var clip := library.get_animation(animation_name)
			if animation_name in ["idle", "walk"]:
				clip.loop_mode = Animation.LOOP_LINEAR
	imported_player.play("idle")
