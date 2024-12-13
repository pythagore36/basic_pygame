import renderer

def update(data, game_data):    
    data["timer"] -= 1
    if data["timer"] < 0:
        game_data["messages"].append({"type":"set_stage", "object":"level_transition"})

def render(data, game_data):    
    renderer.write_text_big("Welcome to this great game !", 250)
    renderer.write_text_middle("By : Pythagore36", 350)    