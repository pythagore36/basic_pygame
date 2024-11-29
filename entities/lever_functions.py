import collision_functions
import pygame
import renderer

ctrl_key_pressed = False

def update(lever_object, level_data):    

    global ctrl_key_pressed

    keys = pygame.key.get_pressed()
        
    if keys[pygame.K_LCTRL] and not ctrl_key_pressed:        
        collisions = collision_functions.collisions(lever_object, level_data)
        player_in_zone = False
        for collision in collisions:
            if collision["type"] == "player":
                player_in_zone = True
        if player_in_zone:
            ctrl_key_pressed = True
            lever_object["state"] ^= 1
    elif not keys[pygame.K_LCTRL]:
        ctrl_key_pressed = False

    return

def render(lever_data, level_data):
    camera_x = level_data["camera"]["x"]
    camera_y = level_data["camera"]["y"]    
    x_draw = lever_data["x"] - camera_x
    y_draw = lever_data["y"] - camera_y
    renderer.draw_image("lever", x_draw, y_draw, image_index=lever_data["state"], centered=True, angle=lever_data["angle"])