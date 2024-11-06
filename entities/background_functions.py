import renderer

def render(level_data):
    camera_x = level_data["camera"]["x"]
    camera_y = level_data["camera"]["y"]
    renderer.draw_image("background", -camera_x, -camera_y)