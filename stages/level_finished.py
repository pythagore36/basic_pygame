import renderer
import data_provider

def update(data, game_data):    
    data["level_name"] = data_provider.get_level_name(game_data["current_level"])
    data["timer"] -= 1
    if data["timer"] < 0:
        if "next_level" in game_data and game_data["next_level"] != None:
            game_data["messages"].append({"type":"change_current_level", "object":game_data["next_level"]})
            game_data["messages"].append({"type":"set_stage", "object":"level_transition"})
        else:
            game_data["messages"].append({"type":"set_stage", "object":"congratulations"})

    

def render(data, game_data):
    renderer.write_text_big("Level completed", 250)
    if "level_name" in data:
        renderer.write_text_middle(data["level_name"], 350)    