def load_door(door_data):
    door = {
        "type":"door",
        "x":door_data["x"],
        "y":door_data["y"],
        "state": "closed",
        "current_image": 0
    }
    return door