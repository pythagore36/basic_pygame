import math
import collision_manager
import renderer

def init(projectile_object):
    global explosion_counter
    model = projectile_object["model"]
    projectile_object["state"] = 'moving'
    direction_x = math.cos(math.radians(projectile_object["angle"]))
    direction_y = -math.sin(math.radians(projectile_object["angle"]))    
    projectile_speed = model["speed"]
    projectile_object["vx"] = direction_x * projectile_speed
    projectile_object["vy"] = direction_y * projectile_speed
    projectile_object["hitboxes"] = model["hitboxes"]    
    explosion_counter = model["explosion_counter"]



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

        collisions = collision_manager.search_collisions(projectile_object, projectile_object["hitboxes"][0], level_data)
        for collision in collisions:
            if collision["collision_type"] == "tile":
                is_collision = True
            if collision["collision_type"] == "entity" and collision["hitbox"]["role"] == "solid" and collision["entity"] != projectile_object["source"]:
                is_collision = True
                if collision["entity"]["type"] in ["player", "enemy"]:         
                    send_damage(collision["entity"], level_data)
        
        if is_collision:
            projectile_object["state"] = 'exploding'
            projectile_object["explosion_counter"] = explosion_counter                
    elif projectile_object["state"] == 'exploding':
        projectile_object["explosion_counter"] -= 1        
        if projectile_object["explosion_counter"] <= 0:
            remove_projectile(projectile_object, level_data)

def render(projectile_object, level_data):
    state = str(projectile_object["state"])
    if "model" in projectile_object and "state_sprites" in projectile_object["model"] and state in projectile_object["model"]["state_sprites"]:
        projectile_object["current_sprite"] = projectile_object["model"]["state_sprites"][state]
        renderer.render_sprite(projectile_object, level_data["camera"])   