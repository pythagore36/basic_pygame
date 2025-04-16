import collision_manager
import entities.utils as utils

def visible(entity1, entity2, level_data):
    fake_entity = {
        "x":0,
        "y":0,
        "angle":0
        }
    hitbox = {
                "type":"poly",
                "points":[{
                    "x":entity1["x"],
                    "y":entity1["y"]
                },{
                    "x":entity2["x"],
                    "y":entity2["y"]
                }]
            }
    collisions = collision_manager.search_collisions(fake_entity, hitbox, level_data)

    for collision in collisions:
        if collision["collision_type"] == "tile":
            return False
        if collision["hitbox"]["role"] == "solid" and collision["entity"] != entity1 and collision["entity"] != entity2:
            return False

    return True

def free_path(entity1, entity2, width, level_data):
    fake_entity = {
        "x":0,
        "y":0,
        "angle":0
        }
    v = (entity2["x"] - entity1["x"], entity2["y"] - entity1["y"])
    v_normal = (-v[1], v[0])
    n = utils.vector_norm(v_normal) * 2
    v_normal = (v_normal[0] * width / n, v_normal[1] * width / n)

    hitbox = {
                "type":"poly",
                "points":[{
                    "x":entity1["x"] + v_normal[0],
                    "y":entity1["y"] + v_normal[1]
                },{
                    "x":entity1["x"] - v_normal[0],
                    "y":entity1["y"] - v_normal[1]
                },{
                    "x":entity2["x"] - v_normal[0],
                    "y":entity2["y"] - v_normal[1]
                },{
                    "x":entity2["x"] + v_normal[0],
                    "y":entity2["y"] + v_normal[1]
                }]
            }
    collisions = collision_manager.search_collisions(fake_entity, hitbox, level_data)

    for collision in collisions:
        if collision["collision_type"] == "tile":
            return False
        if collision["hitbox"]["role"] == "solid" and collision["entity"] != entity1 and collision["entity"] != entity2:
            return False

    return True