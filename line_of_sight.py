import collision_manager

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
         #or collision["hitbox"]["role"] == "solid"

    return True