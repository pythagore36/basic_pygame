import renderer

def update(data, game_data):
    data["timer"] -= 1
    if data["timer"] < 0:
        game_data["messages"].append({"type":"terminate_game", "object":""})


def render(data, game_data):    
    renderer.write_text_big("Congratulations ! You win !", 250)
    renderer.write_text_middle("Thank you for playing", 350)    