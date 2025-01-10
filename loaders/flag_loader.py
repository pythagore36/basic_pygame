import loaders.model_loader as model_loader
import entities.flag_functions as flag_functions

def load_flag(flag_data):
    flag = {
        "type":"flag",
        "x":int(flag_data["x"]),
        "y":int(flag_data["y"])       
    }

    if "angle" in flag_data:
        flag["angle"] = int(flag_data["angle"])
    if "destination" in flag_data:
        flag["destination"] = flag_data["destination"]

    return flag