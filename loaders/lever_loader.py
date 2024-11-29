def load_lever(lever_data):
    lever = {
        "type":"lever",
        "x":lever_data["x"],
        "y":lever_data["y"],
        "angle":lever_data["angle"],
        "hitbox":{
            "x":-16,
            "y":-16,
            "width":32,
            "height":32
        },
        "state": lever_data["state"],
        "id": lever_data["id"]
    }
    return lever