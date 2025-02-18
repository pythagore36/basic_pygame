def init_frame(level_data):
    return

def search_collisions(entity, hitbox, level_data):
    collisions = []

    h = transform(entity, hitbox)
    if h == None:
        return collisions

    #search collisions with entities

    for entity2 in level_data["entities"]:
        if entity == entity2:
            continue
        if "hitboxes" in entity2:
            for hitbox2 in entity2["hitboxes"]:
                h2 = transform(entity2, hitbox2)
                if h2 == None:
                    continue
                if evaluate_collision_transformed(h,h2):
                    collisions.append({
                        "collision_type":"entity",
                        "entity":entity2,
                        "hitbox":hitbox2
                    })

    #search collisions with tilemap

    tilemap = level_data["tilemap_object"]
    bb = h["bounding_box"]

    row1 = int(bb["y1"] / tilemap["tile_height"])
    col1 = int(bb["x1"] / tilemap["tile_width"])
    row2 = int(bb["y2"] / tilemap["tile_height"])
    col2 = int(bb["x2"] / tilemap["tile_width"])

    for row in range(row1, row2+1):
        for col in range(col1, col2+1):
            tile_position = row * tilemap["tile_map_width"] + col
            if tile_position >= 0 and tile_position < len(tilemap["tiles"]) and tilemap["tiles"][tile_position] != 0:
                h_tile = {
                    "type":"AABB",
                    "x": col * tilemap["tile_width"],
                    "y": row * tilemap["tile_height"],
                    "width": tilemap["tile_width"],
                    "height": tilemap["tile_height"]
                }
                if evaluate_collision_transformed(h,h_tile):
                    collisions.append({
                        "collision_type":"tile"
                    })

    return collisions


def transform(entity, hitbox):
    if "type" in hitbox and hitbox["type"] == "AABB":
        return {
            "type":"AABB",
            "x":entity["x"] + hitbox["x"],
            "y":entity["y"] + hitbox["y"],
            "width":hitbox["width"],
            "height":hitbox["height"],
            "bounding_box": {
                "x1": entity["x"] + hitbox["x"],
                "y1": entity["y"] + hitbox["y"],
                "x2": entity["x"] + hitbox["x"] + hitbox["width"],
                "y2": entity["y"] + hitbox["y"] + hitbox["height"]
            }
        }
    return None

def evaluate_collision_transformed(h1, h2):
    if h1["type"] == "AABB" and h2["type"] == "AABB":
        return evaluate_collision_AABB(h1,h2)
    return False

def evaluate_collision_AABB(h1,h2):
    x1 = h1["x"]
    y1 = h1["y"]    
    x2 = h2["x"]
    y2 = h2["y"]
    return not (x2 > x1 + h1["width"] or x1 > x2 + h2["width"] or y2 > y1 + h1["height"] or y1 > y2 + h2["height"])
