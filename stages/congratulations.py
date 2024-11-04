import renderer

def update(game_data):
    game_data["stage"]["timer"] -= 1
    if game_data["stage"]["timer"] < 0:
        game_data["running"] = False


def render(game_data):    
    renderer.write_text_big("Congratulations ! You win !", 250)
    renderer.write_text_middle("Thank you for playing", 350)    