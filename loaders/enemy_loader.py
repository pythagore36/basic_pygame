def load_enemy(enemy_data):
    lever = {
        "type":"enemy",
        "x":int(enemy_data["x"]),
        "y":int(enemy_data["y"]),
        "angle":int(enemy_data["angle"]),
        "hitbox":{
            "x":-45,
            "y":-20,
            "width":90,
            "height":40
        },
        "state":"idle",
        "health" : 3

    }
    return lever