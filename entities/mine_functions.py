import collision_functions
import renderer
import patrolling

def remove_mine(mine_object, level_data):    
    level_data["messages"].append({
        "type":"remove_entity",
        "object":mine_object
    })

def damage_player(level_data, health_points):
    level_data["messages"].append({
        "type":"damage_player",
        "object":health_points
    })

def update(mine_object, level_data):    
    if mine_object["state"] == "patrolling":             
        collisions = collision_functions.collisions(mine_object, level_data)
        
        for collision in collisions:
            if collision["type"] == "player":
                mine_object["state"] = "exploding"
                mine_object["explosion_timer"] = 0
                damage_player(level_data,1)

        mine_object["vx"] = 0
        mine_object["vy"] = 0

        patrolling.apply_patrolling(mine_object)

        mine_object["x"] += mine_object["vx"]
        mine_object["y"] += mine_object["vy"]
    elif mine_object["state"] == 'exploding':
        mine_object["explosion_timer"] += 1
        # si on est arrivé à la fin de l'animation d'explosion, on supprime le projectile
        if mine_object["explosion_timer"] > mine_object["explosion_animation_delay"] * renderer.get_animation_length("explosion"):
            remove_mine(mine_object, level_data)

def image_mine(mine_object):        
    if mine_object["state"] == 'patrolling':
        return ("mine", -1)
    i = int(mine_object["explosion_timer"] / mine_object["explosion_animation_delay"] ) % renderer.get_animation_length("explosion")
    return ("explosion", i)


def render(mine_object, level_data):
    camera_x = level_data["camera"]["x"]
    camera_y = level_data["camera"]["y"]    
    (image_key, image_index) = image_mine(mine_object)
    x_draw = mine_object["x"] - camera_x
    y_draw = mine_object["y"] - camera_y
    renderer.draw_image(image_key, x_draw, y_draw, image_index, True)