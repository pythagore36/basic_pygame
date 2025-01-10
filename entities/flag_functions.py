import collision_functions
import renderer

def init(flag_object):
    flag_object["hitbox"] = flag_object["model"]["hitbox"]
    flag_object["state"] = "not reached"
    flag_object["current_sprite"] = flag_object["model"]["not_reached_sprite"]

def update_not_reached(flag_object, level_data):
    player_object = level_data["entities"][0]   
    if "hitbox" in player_object and collision_functions.is_collision(player_object["x"], player_object["y"], player_object["hitbox"], flag_object["x"], flag_object["y"], flag_object["hitbox"]):
        flag_object["state"] = "reached"
        flag_object["current_sprite"] = flag_object["model"]["reached_sprite"]
        flag_object["reached_countdown_to_exit"] = 60 

def update_reached(flag_object, level_data):
    flag_object["reached_countdown_to_exit"] -= 1
    if flag_object["reached_countdown_to_exit"] < 0:
        finish_level(flag_object, level_data)

def finish_level(flag_object, level_data):
    if "destination" in flag_object:
        level_data["messages"].append({"type":"change_next_level", "object":flag_object["destination"]})
    else:
        level_data["messages"].append({"type":"change_next_level", "object":None})                                
        
    level_data["messages"].append({"type":"set_stage", "object":"level_finished"})

def update(flag_object, level_data):        
    if flag_object["state"] == "not reached":     
        update_not_reached(flag_object, level_data)
    elif flag_object["state"] == "reached":        
         update_reached(flag_object, level_data)

def render(flag_object, level_data):
    renderer.render_sprite(flag_object, level_data["camera"])