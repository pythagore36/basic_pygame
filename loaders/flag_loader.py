def load_flag(flag_data):
    flag = {
        "type":"flag",
        "x":flag_data["x"],
        "y":flag_data["y"],
        "hitbox": {"x":-20,
               "y":-20,
               "width":40,
               "height":40},
        "state": "not reached",
        "reached_countdown_to_exit": 0
    }
    return flag