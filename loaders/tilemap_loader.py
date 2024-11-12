def load_tilemap(tilemap_data):
    tiles_data = tilemap_data["tiles"]
    tile_map_width = len(tiles_data[0].split(","))
    tile_map_height = len(tiles_data)
    tile_width = 32
    tile_height = 32

    tiles = []

    for row in range(tile_map_height):
        row_data = tiles_data[row].split(",")
        for col in range(tile_map_width):
            tiles.append(int(row_data[col]))            

    tilemap = {
        "tile_map_width":tile_map_width,
        "tile_map_height":tile_map_height,
        "tile_width":tile_width,
        "tile_height":tile_height,
        "tiles":tiles
        }
        
    return tilemap