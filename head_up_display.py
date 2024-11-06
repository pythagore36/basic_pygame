import renderer

def render(game_data):
    health = game_data["entities"][0]["health"]
    if health > 0:
        y = 560
        x = 20
        for i in range(health):
            renderer.draw_image("heart", x + 50 * i, y)