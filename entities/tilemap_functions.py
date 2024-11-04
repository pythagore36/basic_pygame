import renderer

def render(tilemap_object, game_data):
    camera_x = game_data["camera"]["x"]
    camera_y = game_data["camera"]["y"]
    for row in range(tilemap_object["tile_map_height"]):
        for col in range(tilemap_object["tile_map_width"]):
            tile_position = row * tilemap_object["tile_map_width"] + col
            tile = tilemap_object["tiles"][tile_position]
            if tile > 0:
                x_tile = col * tilemap_object["tile_width"] - camera_x
                y_tile = row * tilemap_object["tile_height"] - camera_y
                renderer.draw_image("tiles", x_tile, y_tile, image_index=tile-1)   