import collision_manager
import pygame
import renderer

ctrl_key_pressed = False

def update(lever_object, level_data):    

    global ctrl_key_pressed

    if "model" in lever_object:
        lever_object["hitboxes"] = lever_object["model"]["hitboxes"]

    keys = pygame.key.get_pressed()
        
    if keys[pygame.K_LCTRL] and not ctrl_key_pressed:        
        collisions = collision_manager.search_collisions(lever_object,lever_object["hitboxes"][0], level_data)
        player_in_zone = False
        for collision in collisions:
            if collision["collision_type"] == "entity" and collision["entity"]["type"] == "player":
                player_in_zone = True
        if player_in_zone:
            ctrl_key_pressed = True
            lever_object["state"] ^= 1
    elif not keys[pygame.K_LCTRL]:
        ctrl_key_pressed = False

    return

def render(lever_data, level_data):
    state = str(lever_data["state"])
    if "model" in lever_data and "state_sprites" in lever_data["model"] and state in lever_data["model"]["state_sprites"]:
        lever_data["current_sprite"] = lever_data["model"]["state_sprites"][state]
        renderer.render_sprite(lever_data, level_data["camera"])    