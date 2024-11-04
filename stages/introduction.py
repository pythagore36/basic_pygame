import renderer

def update(game_data):    
    game_data["stage"]["timer"] -= 1
    if game_data["stage"]["timer"] < 0:
        game_data["stage"]["name"] = "level"

def render(game_data):    
    renderer.write_text_big("Welcome to this great game !", 250)
    renderer.write_text_middle("By : Pythagore36", 350)    