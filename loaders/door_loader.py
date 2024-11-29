def load_door(door_data):
    door = {
        "type":"door",
        "x":door_data["x"],
        "y":door_data["y"],
        "state": "closed",
        "open_condition": door_data["open_condition"],
        "current_image": 0
    }
    return door