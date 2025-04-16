import math
import sat_collision

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
        return transform_AABB(entity, hitbox)
    if "type" in hitbox and hitbox["type"] == "poly":        
        return transform_poly(entity, hitbox)    
    return None

def transform_AABB(entity, hitbox):
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

def transform_poly(entity, hitbox):
    points = []
        
    for point in hitbox["points"]:
        points.append(point)

    if "angle" in entity:
        angle = entity["angle"]
        for i in range(len(points)):
            point = points[i]
            points[i] = rotatePoint(point, angle)

    for i in range(len(points)):
        point = points[i]
        points[i] = translatePoint(point, entity["x"], entity["y"])

    bounding_box = compute_bounding_box(points)

    result = {
            "type" : "poly",
            "points" : points,
            "bounding_box": bounding_box
        }
    
    return result


def compute_bounding_box(points):
    minX = None
    maxX = None
    minY = None
    maxY = None

    for point in points:
        x = point["x"]
        y = point["y"]
        if minX == None or x < minX:
            minX = x
        if maxX == None or x > maxX:
            maxX = x
        if minY == None or y < minY:
            minY = y
        if maxY == None or y > maxY:
            maxY = y

    bounding_box = {
            "x1":minX,
            "y1":minY,
            "x2":maxX,
            "y2":maxY
        }
    
    return bounding_box

def rotatePoint(point, angle):
    rad = math.radians(angle)
    cos = math.cos(rad)
    sin = math.sin(rad)
    return {
        "x": point["x"] * cos + point["y"] * sin,
        "y": point["y"] * cos - point["x"] * sin
        }

def translatePoint(point, x, y):
    return {
        "x": point["x"] + x,
        "y": point["y"] + y
    }

def evaluate_collision_transformed(h1, h2):
    if h1["type"] == "AABB" and h2["type"] == "AABB":
        return evaluate_collision_AABB(h1,h2)
    if h1["type"] == "poly" and h2["type"] == "poly":
        return evaluate_collision_convex_Polygons(h1,h2)
    if h1["type"] == "AABB" and h2["type"] == "poly":
        return evaluate_collision_convex_polygon_to_AABB(h2,h1)
    if h1["type"] == "poly" and h2["type"] == "AABB":
        return evaluate_collision_convex_polygon_to_AABB(h1,h2)
    return False

def evaluate_collision_AABB(h1,h2):
    x1 = h1["x"]
    y1 = h1["y"]    
    x2 = h2["x"]
    y2 = h2["y"]
    return not (x2 > x1 + h1["width"] or x1 > x2 + h2["width"] or y2 > y1 + h1["height"] or y1 > y2 + h2["height"])

def evaluate_collision_convex_polygon_to_AABB(h_c_poly, h_aabb):
    
    h_aabb_to_poly = {
        "type":"poly",
        "points": [{
            "x":h_aabb["x"],
            "y":h_aabb["y"]
        }, {
            "x":h_aabb["x"] + h_aabb["width"],
            "y":h_aabb["y"]
        }, {
            "x":h_aabb["x"] + h_aabb["width"],
            "y":h_aabb["y"] + h_aabb["height"]
        }, {
            "x":h_aabb["x"],
            "y":h_aabb["y"]  + h_aabb["height"]
        }

        ]
    }    
    
    return evaluate_collision_convex_Polygons(h_c_poly, h_aabb_to_poly)

def evaluate_collision_convex_Polygons(h1,h2):

    points1 = []
    for point in h1["points"]:
        points1.append((point["x"], point["y"]))
    points2 = []
    for point in h2["points"]:
        points2.append((point["x"], point["y"]))

    return sat_collision.polygon_to_polygon(points1, points2)

