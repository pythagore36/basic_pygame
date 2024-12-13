import renderer
import data_provider

def update(data, game_data):    
    data["timer"] -= 1
    if data["timer"] < 0:
        game_data["messages"].append({"type":"set_stage", "object":"level"})
    data["level_name"] = data_provider.get_level_name(game_data["current_level"])

def render(data, game_data):
    renderer.write_text_big("Entering level", 250)
    if "level_name" in data:
        renderer.write_text_middle(data["level_name"], 350)    