import collision_manager
import renderer

def init(flag_object):
    flag_object["hitboxes"] = flag_object["model"]["hitboxes"]
    flag_object["state"] = "not reached"
    flag_object["current_sprite"] = flag_object["model"]["not_reached_sprite"]

def update_not_reached(flag_object, level_data):    
    collisions =  collision_manager.search_collisions(flag_object, flag_object["hitboxes"][0], level_data)
    for collision in collisions:
        if collision["collision_type"] == "entity" and collision["entity"]["type"] == "player":
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