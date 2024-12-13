import collision_functions
import renderer

def update(flag_object, level_data):    
    player_object = level_data["entities"][0]
    if flag_object["state"] == "not reached":
        if "hitbox" in player_object and collision_functions.is_collision(player_object["x"], player_object["y"], player_object["hitbox"], flag_object["x"], flag_object["y"], flag_object["hitbox"]):
            flag_object["state"] = "reached"
            flag_object["reached_countdown_to_exit"] = 60            
    elif flag_object["state"] == "reached":
        flag_object["reached_countdown_to_exit"] -= 1
        if flag_object["reached_countdown_to_exit"] < 0:
            if "destination" in flag_object:
                level_data["messages"].append({"type":"change_next_level", "object":flag_object["destination"]})
            else:
                level_data["messages"].append({"type":"change_next_level", "object":None})                                
                
            level_data["messages"].append({"type":"set_stage", "object":"level_finished"})                        

def render(flag_object, level_data):
    camera_x = level_data["camera"]["x"]
    camera_y = level_data["camera"]["y"]
    if flag_object["state"]=="not reached":        
        x_draw = flag_object["x"] - camera_x
        y_draw = flag_object["y"] - camera_y
        renderer.draw_image("flag", x_draw, y_draw, centered=True)