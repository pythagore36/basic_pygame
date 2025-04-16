import renderer
import entities.utils as utils
import math
import line_of_sight
import collision_manager

def init(enemy_object):    
    model = enemy_object["model"]
    enemy_object["activation_distance"] = model["activation_distance"]
    enemy_object["delay_between_shoots"] = model["delay_between_shoots"]
    enemy_object["projectile_model"] = model["projectile_model"]
    enemy_object["health"] = model["health"]
    enemy_object["hitboxes"] = model["hitboxes"]
    enemy_object["explosion_counter"] = model["explosion_counter"]
    if "speed" in model:
        enemy_object["speed"] = model["speed"]
    else:
        enemy_object["speed"] = 0
    if "target_distance" in model:
        enemy_object["target_distance"] = model["target_distance"]    
    enemy_object["target"] = None
    if "path_width" in model:
        enemy_object["path_width"] = model["path_width"]
    else:
        enemy_object["path_width"] = 1

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
        if distance < enemy_object["activation_distance"] and line_of_sight.visible(enemy_object, player_object, level_data):
            enemy_object["state"] = "active"
            enemy_object["shoot_countdown"] = enemy_object["delay_between_shoots"]
            enemy_object["target"] = player_object
            enemy_object["angle"] = utils.angle_to_target(enemy_object, enemy_object["target"]) 
            enemy_object["choose_target_countdown"] = 60
            
    if enemy_object["state"] == "active":
        # choose target
        enemy_object["choose_target_countdown"] -= 1
        if enemy_object["choose_target_countdown"] < 0 or enemy_object["target"] == None:
            enemy_object["choose_target_countdown"] = 60
            enemy_object["target"] = player_object
            if not line_of_sight.free_path(enemy_object, player_object, enemy_object["path_width"], level_data) and "positions" in player_object:
                for position in player_object["positions"]:
                    if line_of_sight.free_path(enemy_object, position, enemy_object["path_width"], level_data) and utils.distance(enemy_object, position) > 50:
                        enemy_object["target"] = position
                        break
            # orient toward target
            enemy_object["angle"] = utils.angle_to_target(enemy_object, enemy_object["target"])            
        
        
        # shoot only if path to player is free
        if line_of_sight.free_path(enemy_object, player_object, enemy_object["path_width"], level_data):
            enemy_object["shoot_countdown"]-=1
            if enemy_object["shoot_countdown"] < 0:
                enemy_object["shoot_countdown"] = enemy_object["delay_between_shoots"]
                enemy_object["angle"] = utils.angle_to_target(enemy_object, enemy_object["target"])
                shoot_projectile(enemy_object, level_data)         

        # if too far from player, deactivate
        if distance >= enemy_object["activation_distance"]:
            enemy_object["state"] = "idle"
            enemy_object["target"] = None
        
        if enemy_object["target"]  != None and "target_distance" in enemy_object and distance > enemy_object["target_distance"] and enemy_object["speed"] > 0:
            move_towards_target(enemy_object, enemy_object["target"] , level_data)
    
    if enemy_object["state"] == "hurt":
        enemy_object["hurt_timer"]-=1
        if enemy_object["hurt_timer"] <= 0:
            enemy_object["state"] = "active"
    
    if enemy_object["state"] == 'exploding':
        enemy_object["explosion_timer"] -= 1
        
        if enemy_object["explosion_timer"] <= 0:
            remove_enemy(enemy_object, level_data)

    return

def move_towards_target(entity, target, level_data):
    
    speed = entity["speed"]

    vx = speed * math.cos(math.radians(entity["angle"]))
    vy = -speed * math.sin(math.radians(entity["angle"]))

    entity["x"] += vx
    if solid_collision(entity, level_data):
        entity["x"]-=vx
    
    entity["y"] += vy
    if solid_collision(entity, level_data):
        entity["y"]-=vy
    
    return

def solid_collision(entity, level_data):
    collisions = collision_manager.search_collisions(entity, entity["hitboxes"][0], level_data)

    for collision in collisions:
        if collision["collision_type"] == "tile":
            return True
        if collision["collision_type"] == "entity" and collision["hitbox"]["role"] == "solid":
            return True

    return False

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