import collision_functions
import renderer

def remove_projectile(projectile_object, game_data):    
    game_data["messages"].append({
        "type":"remove_projectile",
        "object":projectile_object
    })


def update(projectile_object, game_data):
    tilemap_object = game_data["tilemap_object"]
    # si le projectile est à l'état "moving" il continue d'avance selon sa vitesse en x et en y.
    if projectile_object["state"] == 'moving':
        projectile_object["x"] += projectile_object["vx"]
        projectile_object["y"] += projectile_object["vy"]
        projectile_object["moving_timer"] -= 1
        # si le projectile est arrivé à la fin de sa durée de vie ou qu'il a touché un obstacle solide, il passe en mode "exploding"
        if projectile_object["moving_timer"] <= 0 or collision_functions.is_collision_with_tilemap(projectile_object["x"], projectile_object["y"], projectile_object["hitbox"], tilemap_object):
            projectile_object["state"] = 'exploding'
            projectile_object["explosion_timer"] = 0            
    # si le projectile est en mode "exploding", on augmente le timer de l'explosion  pour qu'on sache à quelle image on en est.
    elif projectile_object["state"] == 'exploding':
        projectile_object["explosion_timer"] += 1
        # si on est arrivé à la fin de l'animation d'explosion, on supprime le projectile
        if projectile_object["explosion_timer"] > projectile_object["explosion_animation_delay"] * renderer.get_animation_length("explosion"):
            remove_projectile(projectile_object, game_data)

def image_projectile(projectile_object, game_data):        
    if projectile_object["state"] == 'moving':
        return ("fireball", -1)    
    i = int(projectile_object["explosion_timer"] / projectile_object["explosion_animation_delay"] ) % renderer.get_animation_length("explosion")
    return ("explosion", i)

def render(projectile_object, game_data):
    camera_x = game_data["camera"]["x"]
    camera_y = game_data["camera"]["y"]    
    (image_key, image_index) = image_projectile(projectile_object, game_data)
    x_draw = projectile_object["x"] - camera_x
    y_draw = projectile_object["y"] - camera_y
    renderer.draw_image(image_key, x_draw, y_draw, image_index, True, projectile_object["angle"] )  