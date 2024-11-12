def load_player(player_data):
    player = {
        "type":"player",
        "x":player_data["x"],
        "y":player_data["y"],
        "angle":player_data["angle"],
        "vx":0,
        "vy":0,
        "health":3,
        "state":"alive",
        "hitbox": {"x":-15,
               "y":-15,
               "width":30,
               "height":30},
        "next_projectile_delay":0,
        "explosion_animation_delay":3
    }
    return player