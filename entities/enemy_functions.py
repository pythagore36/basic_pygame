import renderer
import entities.utils as utils
import math

def init(enemy_object):    
    model = enemy_object["model"]
    enemy_object["activation_distance"] = model["activation_distance"]
    enemy_object["delay_between_shoots"] = model["delay_between_shoots"]
    enemy_object["projectile_model"] = model["projectile_model"]
    enemy_object["health"] = model["health"]
    enemy_object["hitboxes"] = model["hitboxes"]
    enemy_object["explosion_counter"] = model["explosion_counter"]


def apply_message(message):
    message_object = message["object"]
    entity = message["to"]
    if message_object["title"] == "damage":
        entity["health"]-=message_object["health_points"]
    if entity["health"] <= 0:
        entity["state"] = "exploding"
        entity["explosion_timer"] = entity["explosion_counter"]
        del entity["hitboxes"]
    else:
        entity["state"] = "hurt"
        entity["hurt_timer"] = 60
    return

def remove_enemy(enemy_object, level_data):
    level_data["messages"].append({
        "type":"remove_entity",
        "object":enemy_object
    })

def shoot_projectile(enemy_object, level_data):
          
    projectile_data = {}

    direction_x = math.cos(math.radians(enemy_object["angle"]))
    direction_y = -math.sin(math.radians(enemy_object["angle"]))
    projectile_data["type"] = "projectile"
    projectile_data["source"] = enemy_object
    projectile_data["x"] = enemy_object["x"] + direction_x * 30
    projectile_data["y"] = enemy_object["y"] + direction_y * 30    
    projectile_data["angle"] = enemy_object["angle"]
    projectile_data["model"] = enemy_object["projectile_model"]

    level_data["messages"].append({
        "type":"add_entity",
        "object":projectile_data
    })


def update(enemy_object, level_data):  
    player_object = level_data["entities"][0]
    distance = utils.distance(enemy_object, player_object)
    if enemy_object["state"] == "idle":
        if distance < enemy_object["activation_distance"]:
            enemy_object["state"] = "active"
            enemy_object["shoot_countdown"] = enemy_object["delay_between_shoots"]
            
    if enemy_object["state"] == "active":
        enemy_object["angle"] = utils.angle_to_target(enemy_object, player_object)
        
        enemy_object["shoot_countdown"]-=1
        if enemy_object["shoot_countdown"] < 0:
           enemy_object["shoot_countdown"] = enemy_object["delay_between_shoots"]
           shoot_projectile(enemy_object, level_data) 

        if distance >= enemy_object["activation_distance"]:
            enemy_object["state"] = "idle"
    
    if enemy_object["state"] == "hurt":
        enemy_object["hurt_timer"]-=1
        if enemy_object["hurt_timer"] <= 0:
            enemy_object["state"] = "idle"
    
    if enemy_object["state"] == 'exploding':
        enemy_object["explosion_timer"] -= 1
        
        if enemy_object["explosion_timer"] <= 0:
            remove_enemy(enemy_object, level_data)

    return


def compute_image(enemy_object):        
    state = str(enemy_object["state"])
    if "model" in enemy_object and "state_sprites" in enemy_object["model"] and state in enemy_object["model"]["state_sprites"]:
        enemy_object["current_sprite"] = enemy_object["model"]["state_sprites"][state]

    if enemy_object["state"] == 'hurt':
        i = int(enemy_object["hurt_timer"] / 3)
        if i%2 == 0:
            enemy_object["current_sprite"] = None

def render(enemy_object, level_data):
    compute_image(enemy_object)
    if enemy_object["current_sprite"] != None:
        renderer.render_sprite(enemy_object, level_data["camera"])