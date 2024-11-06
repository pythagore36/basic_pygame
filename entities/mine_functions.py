import collision_functions
import renderer
import patrolling

def remove_mine(mine_object, game_data):    
    game_data["messages"].append({
        "type":"remove_mine",
        "object":mine_object
    })

def damage_player(game_data, health_points):
    game_data["messages"].append({
        "type":"damage_player",
        "object":health_points
    })

def update(mine_object, game_data):
    player_object = game_data["player_object"]
    if mine_object["state"] == "patrolling":             
        if collision_functions.is_collision(mine_object["x"], mine_object["y"], mine_object["hitbox"],player_object["x"], player_object["y"], player_object["hitbox"]):
            mine_object["state"] = "exploding"
            mine_object["explosion_timer"] = 0
            damage_player(game_data,1)

        mine_object["vx"] = 0
        mine_object["vy"] = 0

        patrolling.apply_patrolling(mine_object)

        mine_object["x"] += mine_object["vx"]
        mine_object["y"] += mine_object["vy"]
    elif mine_object["state"] == 'exploding':
        mine_object["explosion_timer"] += 1
        # si on est arrivé à la fin de l'animation d'explosion, on supprime le projectile
        if mine_object["explosion_timer"] > mine_object["explosion_animation_delay"] * renderer.get_animation_length("explosion"):
            remove_mine(mine_object, game_data)

def image_mine(mine_object):        
    if mine_object["state"] == 'patrolling':
        return ("mine", -1)
    i = int(mine_object["explosion_timer"] / mine_object["explosion_animation_delay"] ) % renderer.get_animation_length("explosion")
    return ("explosion", i)


def render(mine_object, game_data):
    camera_x = game_data["camera"]["x"]
    camera_y = game_data["camera"]["y"]    
    (image_key, image_index) = image_mine(mine_object)
    x_draw = mine_object["x"] - camera_x
    y_draw = mine_object["y"] - camera_y
    renderer.draw_image(image_key, x_draw, y_draw, image_index, True)