import pygame
import collision_manager
import renderer
import math

POSITIONS_SIZE = 40
POSITIONS_DELAY = 15

def init(player_object):
    model = player_object["model"]

    player_object["vx"] = 0
    player_object["vy"] = 0
    player_object["state"] = "alive"
    player_object["next_projectile_delay"] = 0
    player_object["health"] = model["health"]
    player_object["delay_between_shoots"] = model["delay_between_shoots"]
    player_object["explosion_counter"] = model["explosion_counter"]
    player_object["speed"] = model["speed"]
    player_object["rotation_speed"] = model["rotation_speed"]
    player_object["hitboxes"] = model["hitboxes"]
    
    player_object["positions"] = []
    player_object["store_next_position_countdown"] = POSITIONS_DELAY

def apply_message(message):
    message_object = message["object"]
    if message_object["title"] == "damage":
        damage_player(message["to"], message_object["health_points"])
    return


def add_projectile(player_object, level_data):
          
    projectile_data = {}

    direction_x = math.cos(math.radians(player_object["angle"]))
    direction_y = -math.sin(math.radians(player_object["angle"]))
    projectile_data["type"] = "projectile"
    projectile_data["source"] = player_object
    projectile_data["x"] = player_object["x"] + direction_x * 10
    projectile_data["y"] = player_object["y"] + direction_y * 10
    projectile_data["angle"] = player_object["angle"]
    projectile_data["model"] = "player_projectile"


    level_data["messages"].append({
        "type":"add_entity",
        "object":projectile_data
    })

    player_object["next_projectile_delay"] = player_object["delay_between_shoots"]


def damage_player(player_object, health_points):
    
    player_object["health"]-=health_points
    if player_object["health"] <= 0:
        player_object["state"] = "exploding"
        player_object["explosion_timer"] = player_object["explosion_counter"] 
        del player_object["hitboxes"]
    else:
        player_object["state"] = "hurt"
        player_object["hurt_timer"] = 60
        

def update(player_object, level_data):    
    
    player_object["store_next_position_countdown"] -= 1
    if player_object["store_next_position_countdown"] < 0:
        player_object["store_next_position_countdown"] = POSITIONS_DELAY
        player_object["positions"].insert(0, {"x":player_object["x"], "y":player_object["y"]})
        if len(player_object["positions"]) > POSITIONS_SIZE:
            player_object["positions"].pop()

    if player_object["state"] == "exploding":
        player_object["explosion_timer"] -= 1
        if player_object["explosion_timer"] <= 0:
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

    player_object["vx"] = 0
    player_object["vy"] = 0
    
    speed = player_object["speed"]
    rotation_speed = player_object["rotation_speed"]

    if keys[pygame.K_LEFT]:
        if keys[pygame.K_LALT]:
            player_object["vx"] += speed * math.cos(math.radians(player_object["angle"] + 90))
            player_object["vy"] += -speed * math.sin(math.radians(player_object["angle"] + 90))
        else:            
            player_object["angle"]+=rotation_speed
    if keys[pygame.K_RIGHT]:
        if keys[pygame.K_LALT]:
            player_object["vx"] += speed * math.cos(math.radians(player_object["angle"] - 90))
            player_object["vy"] += -speed * math.sin(math.radians(player_object["angle"] - 90))
        else: 
            player_object["angle"]-=rotation_speed

    # on crée un projectile si la touche espace est pressée
    if keys[pygame.K_SPACE] and player_object["next_projectile_delay"] <= 0 :
        add_projectile(player_object, level_data)

    # la vitesse de déplacement du joueur en x et y est décidée selon les appuis sur les touches haut et bas et selon l'angle courant du joueur. Détail à étudier ensemble.
    if keys[pygame.K_UP]:
        player_object["vx"] += speed * math.cos(math.radians(player_object["angle"]))
        player_object["vy"] += -speed * math.sin(math.radians(player_object["angle"]))
    elif keys[pygame.K_DOWN]: 
        player_object["vx"] += -speed * math.cos(math.radians(player_object["angle"]))
        player_object["vy"] += speed * math.sin(math.radians(player_object["angle"]))
        
    
    # on appelle la fonction de déplacement du joueur après avoir calculé sa vitesse
    move_player(player_object, level_data)

    if player_object["next_projectile_delay"] > 0:
        player_object["next_projectile_delay"]-=1


def solid_collision(player_object, level_data):
    collisions = collision_manager.search_collisions(player_object, player_object["hitboxes"][0], level_data)

    for collision in collisions:
        if collision["collision_type"] == "tile":
            return True
        if collision["collision_type"] == "entity" and collision["hitbox"]["role"] == "solid":
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

def compute_image(player_object):        
    state = str(player_object["state"])
    if "model" in player_object and "state_sprites" in player_object["model"] and state in player_object["model"]["state_sprites"]:
        player_object["current_sprite"] = player_object["model"]["state_sprites"][state]

    if player_object["state"] == 'hurt':
        i = int(player_object["hurt_timer"] / 3)
        if i%2 == 0:
            player_object["current_sprite"] = None


def render(player_object, level_data):
    compute_image(player_object)
    if player_object["current_sprite"] != None:
        renderer.render_sprite(player_object, level_data["camera"])

