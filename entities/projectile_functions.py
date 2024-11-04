import math
import collision_functions
import renderer

# fonction qui supprime le projectile à la fin de l'animation d'explosion. Il suffit de mettre le boolean has_projectile à False
def remove_projectile(projectile_object):    
    projectile_object["has_projectile"] = False

# fonction qui crée un projectile depuis l'emplacement courant du joueur et avec l'angle courant du joueur. Contenu de la fonction à étudier ensemble.
def add_projectile(projectile_object, game_data):    
    player_object = game_data["player_object"]
    projectile_object["has_projectile"] = True
    direction_x = math.cos(math.radians(player_object["angle"]))
    direction_y = -math.sin(math.radians(player_object["angle"]))
    projectile_object["x"] = player_object["x"] + direction_x * 10
    projectile_object["y"] = player_object["y"] + direction_y * 10
    projectile_object["state"] = 'moving'
    projectile_object["angle"] = player_object["angle"]
    projectile_object["moving_timer"] = 300
    projectile_object["vx"] = direction_x * 10
    projectile_object["vy"] = direction_y * 10

# fonction qui met à jour le projectile  à chaque frame s'il existe
def update(projectile_object, game_data):
    if not projectile_object["has_projectile"]:
        return 
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
            remove_projectile(projectile_object)

def image_projectile(game_data):    
    projectile_object = game_data["projectile_object"]    
    if projectile_object["state"] == 'moving':
        return ("fireball", -1)    
    i = int(projectile_object["explosion_timer"] / projectile_object["explosion_animation_delay"] ) % renderer.get_animation_length("explosion")
    return ("explosion", i)

def render(projectile_object, game_data):
    camera_x = game_data["camera"]["x"]
    camera_y = game_data["camera"]["y"]
    if projectile_object["has_projectile"] :
        (image_key, image_index) = image_projectile(game_data)
        x_draw = projectile_object["x"] - camera_x
        y_draw = projectile_object["y"] - camera_y
        renderer.draw_image(image_key, x_draw, y_draw, image_index, True, projectile_object["angle"] )  