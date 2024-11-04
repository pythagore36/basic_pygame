import renderer

def render(game_data):
    camera_x = game_data["camera"]["x"]
    camera_y = game_data["camera"]["y"]
    renderer.draw_image("background", -camera_x, -camera_y)