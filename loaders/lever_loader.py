import loaders.model_loader as model_loader

def load_lever(lever_data):
    lever = {
        "type":"lever",
        "x":int(lever_data["x"]),
        "y":int(lever_data["y"]),
        "angle":int(lever_data["angle"]),
        "state": int(lever_data["state"]),
        "id": int(lever_data["id"])
    }

    return lever