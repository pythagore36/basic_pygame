import renderer

scroll_x_weight = 0.1
scroll_y_weight = 0

screen_width = 608
screen_height = 608

def render(level_data):
    camera_x = level_data["camera"]["x"]
    camera_y = level_data["camera"]["y"]

    image_width = renderer.get_image_size("background")[0]
    image_height = renderer.get_image_size("background")[1]
    
    draw_x = int(-scroll_x_weight * camera_x)

    while draw_x < screen_width:
        draw_y = int(-scroll_y_weight * camera_y)
        while draw_y < screen_height:
            renderer.draw_image("background", draw_x, draw_y)
            draw_y += image_height
        draw_x += image_width