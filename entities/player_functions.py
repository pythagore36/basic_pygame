import pygame
import collision_functions
import renderer
import math


def apply_message(message):
    message_object = message["object"]
    if message_object["title"] == "damage":
        damage_player(message["to"], message_object["health_points"])
    return


def add_projectile(player_object, level_data):
          
    projectile_object = {}

    direction_x = math.cos(math.radians(player_object["angle"]))
    direction_y = -math.sin(math.radians(player_object["angle"]))
    projectile_object["type"] = "projectile"
    projectile_object["source"] = player_object
    projectile_object["x"] = player_object["x"] + direction_x * 10
    projectile_object["y"] = player_object["y"] + direction_y * 10
    projectile_object["state"] = 'moving'
    projectile_object["angle"] = player_object["angle"]
    projectile_object["moving_timer"] = 300
    projectile_object["vx"] = direction_x * 10
    projectile_object["vy"] = direction_y * 10
    projectile_object["hitbox"] = {"x":-15, "y":-15, "width":30, "height":30}
    projectile_object["explosion_animation_delay"] = 3

    level_data["messages"].append({
        "type":"add_entity",
        "object":projectile_object
    })

    player_object["next_projectile_delay"] = 10


def damage_player(player_object, health_points):
    
    player_object["health"]-=health_points
    if player_object["health"] <= 0:
        player_object["state"] = "exploding"
        player_object["explosion_timer"] = 0
        del player_object["hitbox"]
    else:
        player_object["state"] = "hurt"
        player_object["hurt_timer"] = 60
        

def update(player_object, level_data):    
    
    if player_object["state"] == "exploding":
        player_object["explosion_timer"] += 1
        if player_object["explosion_timer"] > player_object["explosion_animation_delay"] * renderer.get_animation_length("explosion"):
            level_data["messages"].append({"type":"set_stage", "object":"game_over"})
        return
    
    if player_object["state"] == "hurt":
        player_object["hurt_timer"]-=1
        if player_object["hurt_timer"] <= 0:
            player_object["state"] = "alive"

    #fonction pygame qui nous permet de savoir quelles touches du clavier sont pressées en ce moment. keys[une certaine touche] sera True si cette touche est pressée, False sinon    
    keys = pygame.key.get_pressed()
    
    if keys[pygame.K_c]:
        print("current position :", player_object["x"], player_object["y"])


    # les appuis sur les touches gauche et droite modifient l'angle courant du joueur.
    if keys[pygame.K_LEFT]: 
        player_object["angle"]+=5
    if keys[pygame.K_RIGHT]: 
        player_object["angle"]-=5

    # on crée un projectile si la touche espace est pressée
    if keys[pygame.K_SPACE] and player_object["next_projectile_delay"] <= 0 :
        add_projectile(player_object, level_data)

    # la vitesse de déplacement du joueur en x et y est décidée selon les appuis sur les touches haut et bas et selon l'angle courant du joueur. Détail à étudier ensemble.
    if keys[pygame.K_UP]:
        player_object["vx"] = 5 * math.cos(math.radians(player_object["angle"]))
        player_object["vy"] = -5 * math.sin(math.radians(player_object["angle"]))
    elif keys[pygame.K_DOWN]: 
        player_object["vx"] = -5 * math.cos(math.radians(player_object["angle"]))
        player_object["vy"] = 5 * math.sin(math.radians(player_object["angle"]))
    else:
        player_object["vx"] = 0
        player_object["vy"] = 0
    
    # on appelle la fonction de déplacement du joueur après avoir calculé sa vitesse
    move_player(player_object, level_data)

    if player_object["next_projectile_delay"] > 0:
        player_object["next_projectile_delay"]-=1


def solid_collision(player_object, level_data):
    tilemap_object = level_data["tilemap_object"]
    if collision_functions.is_collision_with_tilemap(player_object["x"], player_object["y"], player_object["hitbox"], tilemap_object):
        return True
    collisions = collision_functions.collisions(player_object, level_data)
    for collision in collisions:
        if collision["type"] in ["door", "enemy"]:
            return True    
    return False

# Cette fonction déplace le joueur à chaque frame. Deux mouvements sont effectués : un mouvement selon x et l'autre selon y.
# Dans chaque cas, si une collision est détectée après le mouvement, le mouvement est annulé et on reste dans la position actuelle.
def move_player(player_object, level_data):        
    player_object["x"] += player_object["vx"]
    if solid_collision(player_object, level_data):
        player_object["x"]-=player_object["vx"]
    player_object["y"] += player_object["vy"]
    if solid_collision(player_object, level_data):
        player_object["y"]-=player_object["vy"]

def image_player(player_object):        
    if player_object["state"] == 'alive':
        return ("player", -1)
    elif player_object["state"] == 'exploding':
        i = int(player_object["explosion_timer"] / player_object["explosion_animation_delay"] ) % renderer.get_animation_length("explosion")
        return ("explosion", i)
    elif player_object["state"] == 'hurt':
        i = int(player_object["hurt_timer"] / 3)
        if i%2 == 0:
            return ("player", -1)
        else:
            return ("null", -1)

def render(player_object, level_data):
    camera_x = level_data["camera"]["x"]
    camera_y = level_data["camera"]["y"]
    x_draw = player_object["x"] - camera_x
    y_draw = player_object["y"] - camera_y
    (image_key, image_index) = image_player(player_object)
    renderer.draw_image(image_key, x_draw, y_draw, image_index, centered=True, angle=player_object["angle"])