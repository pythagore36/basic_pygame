import collision_functions
import renderer

def remove_projectile(projectile_object, level_data):    
    level_data["messages"].append({
        "type":"remove_entity",
        "object":projectile_object
    })

def send_damage(entity, level_data):
    level_data["messages"].append({
        "type":"entity",
        "to":entity,
        "object":{
            "title":"damage",
            "health_points": 1
        }
        }
    )

def update(projectile_object, level_data):
    tilemap_object = level_data["tilemap_object"]
    # si le projectile est à l'état "moving" il continue d'avance selon sa vitesse en x et en y.
    if projectile_object["state"] == 'moving':
        projectile_object["x"] += projectile_object["vx"]
        projectile_object["y"] += projectile_object["vy"]        
        
        is_collision = False

        collisions = collision_functions.collisions(projectile_object, level_data)
        for collision in collisions:
            if collision["type"] in ["mine", "flag", "door"]:
                is_collision = True
            if collision["type"] in ["player", "enemy"] and collision != projectile_object["source"] :
                is_collision = True
                send_damage(collision, level_data)


        if collision_functions.is_collision_with_tilemap(projectile_object["x"], projectile_object["y"], projectile_object["hitbox"], tilemap_object):
            is_collision = True
        
        if is_collision:
            projectile_object["state"] = 'exploding'
            projectile_object["explosion_timer"] = 0            
    # si le projectile est en mode "exploding", on augmente le timer de l'explosion  pour qu'on sache à quelle image on en est.
    elif projectile_object["state"] == 'exploding':
        projectile_object["explosion_timer"] += 1
        # si on est arrivé à la fin de l'animation d'explosion, on supprime le projectile
        if projectile_object["explosion_timer"] > projectile_object["explosion_animation_delay"] * renderer.get_animation_length("explosion"):
            remove_projectile(projectile_object, level_data)

def image_projectile(projectile_object, level_data):        
    if projectile_object["state"] == 'moving':
        return ("fireball", -1)    
    i = int(projectile_object["explosion_timer"] / projectile_object["explosion_animation_delay"] ) % renderer.get_animation_length("explosion")
    return ("explosion", i)

def render(projectile_object, level_data):
    camera_x = level_data["camera"]["x"]
    camera_y = level_data["camera"]["y"]    
    (image_key, image_index) = image_projectile(projectile_object, level_data)
    x_draw = projectile_object["x"] - camera_x
    y_draw = projectile_object["y"] - camera_y
    renderer.draw_image(image_key, x_draw, y_draw, image_index, True, projectile_object["angle"] )  