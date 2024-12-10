def load_flag(flag_data):
    flag = {
        "type":"flag",
        "x":int(flag_data["x"]),
        "y":int(flag_data["y"]),        
        "hitbox": {"x":-20,
               "y":-20,
               "width":40,
               "height":40},
        "state": "not reached",
        "reached_countdown_to_exit": 0
    }

    if "angle" in flag_data:
        flag["angle"] = int(flag_data["angle"])

    return flag