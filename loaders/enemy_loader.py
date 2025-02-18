def load_enemy(enemy_data):
    lever = {
        "type":"enemy",
        "x":int(enemy_data["x"]),
        "y":int(enemy_data["y"]),
        "angle":int(enemy_data["angle"]),
        "state":"idle",
        "health" : 3

    }
    return lever