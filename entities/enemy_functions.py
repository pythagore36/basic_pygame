import renderer
import entities.utils as utils
import math

activation_distance = 400
delay_between_shoots = 90
projectile_speed = 5


def apply_message(message):
    message_object = message["object"]
    entity = message["to"]
    if message_object["title"] == "damage":
        entity["health"]-=message_object["health_points"]
    if entity["health"] <= 0:
        entity["state"] = "exploding"
        entity["explosion_timer"] = 0
        entity["explosion_animation_delay"] = 3
        del entity["hitbox"]
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
          
    projectile_object = {}

    direction_x = math.cos(math.radians(enemy_object["angle"]))
    direction_y = -math.sin(math.radians(enemy_object["angle"]))
    projectile_object["type"] = "projectile"
    projectile_object["source"] = enemy_object
    projectile_object["x"] = enemy_object["x"] + direction_x * 30
    projectile_object["y"] = enemy_object["y"] + direction_y * 30
    projectile_object["state"] = 'moving'
    projectile_object["angle"] = enemy_object["angle"]
    projectile_object["moving_timer"] = 300
    projectile_object["vx"] = direction_x * projectile_speed
    projectile_object["vy"] = direction_y * projectile_speed
    projectile_object["hitbox"] = {"x":-15, "y":-15, "width":30, "height":30}
    projectile_object["explosion_animation_delay"] = 3

    level_data["messages"].append({
        "type":"add_entity",
        "object":projectile_object
    })


def update(enemy_object, level_data):  
    player_object = level_data["entities"][0]
    distance = utils.distance(enemy_object, player_object)
    if enemy_object["state"] == "idle":
        if distance < activation_distance:
            enemy_object["state"] = "active"
            enemy_object["shoot_countdown"] = delay_between_shoots
            
    if enemy_object["state"] == "active":
        enemy_object["angle"] = utils.angle_to_target(enemy_object, player_object)
        
        enemy_object["shoot_countdown"]-=1
        if enemy_object["shoot_countdown"] < 0:
           enemy_object["shoot_countdown"] = delay_between_shoots
           shoot_projectile(enemy_object, level_data) 

        if distance >= activation_distance:
            enemy_object["state"] = "idle"
    
    if enemy_object["state"] == "hurt":
        enemy_object["hurt_timer"]-=1
        if enemy_object["hurt_timer"] <= 0:
            enemy_object["state"] = "idle"
    
    if enemy_object["state"] == 'exploding':
        enemy_object["explosion_timer"] += 1
        
        if enemy_object["explosion_timer"] > enemy_object["explosion_animation_delay"] * renderer.get_animation_length("explosion"):
            remove_enemy(enemy_object, level_data)

    return


def image_enemy(enemy_object):        
    if enemy_object["state"] in ["active", "idle"]:
        return ("turret", -1)
    elif enemy_object["state"] == 'exploding':
        i = int(enemy_object["explosion_timer"] / enemy_object["explosion_animation_delay"] ) % renderer.get_animation_length("explosion")
        return ("explosion", i)
    elif enemy_object["state"] == 'hurt':
        i = int(enemy_object["hurt_timer"] / 3)
        if i%2 == 0:
            return ("turret", -1)
        else:
            return ("null", -1)

def render(enemy_object, level_data):
    camera_x = level_data["camera"]["x"]
    camera_y = level_data["camera"]["y"]    
    (image_key, image_index) = image_enemy(enemy_object)
    x_draw = enemy_object["x"] - camera_x
    y_draw = enemy_object["y"] - camera_y
    renderer.draw_image(image_key, x_draw, y_draw, image_index=image_index, centered=True, angle=enemy_object["angle"])