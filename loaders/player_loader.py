def load_player(player_data):
    player = {
        "type":"player",
        "x":int(player_data["x"]),
        "y":int(player_data["y"]),
        "angle":int(player_data["angle"])
    }
    return player