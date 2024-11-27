import collision_functions
import pygame
import renderer

number_of_images = 7
closed_image = 0
open_image = 6
animation_delay = 3

hitbox_closed = {
    "x":-32,
    "y":-32,
    "width":64,
    "height":64
}

hitbox_open = {
    "x":-32,
    "y":-32,
    "width":64,
    "height":1
}

def open(door_object):
    if door_object["state"] == "closed":
        door_object["state"] = "opening"
        door_object["counter"] = 0

def close(door_object, level_data):
    if door_object["state"] == "open":
        door_object["hitbox"] = hitbox_closed

        # door cannot close if something is under it
        collisions = collision_functions.collisions(door_object, level_data)
        for collision in collisions:
            if collision["type"] in ["player"]:
                door_object["hitbox"] = hitbox_open
                return

        door_object["state"] = "closing"
        door_object["counter"] = 0

def update(door_object, level_data):    
    
    if "hitbox" not in door_object:
        if door_object["state"] == "open":
            door_object["hitbox"] = hitbox_open
        else :
            door_object["hitbox"] = hitbox_closed

    if door_object["state"] == "opening":
        door_object["counter"] += 1
        if door_object["counter"] > animation_delay:
            door_object["current_image"] += 1
            door_object["counter"] = 0
        if door_object["current_image"] == open_image:
            door_object["state"] = "open"
            door_object["hitbox"] = hitbox_open
    
    if door_object["state"] == "closing":
        door_object["counter"] += 1
        if door_object["counter"] > animation_delay:
            door_object["current_image"] -= 1
            door_object["counter"] = 0
        if door_object["current_image"] == closed_image:
            door_object["state"] = "closed"
            
    
    keys = pygame.key.get_pressed()
        
    if keys[pygame.K_o]: 
        open(door_object)
    if keys[pygame.K_c]: 
        close(door_object, level_data)

    return

def render(door_object, level_data):
    camera_x = level_data["camera"]["x"]
    camera_y = level_data["camera"]["y"]    
    x_draw = door_object["x"] - camera_x
    y_draw = door_object["y"] - camera_y
    renderer.draw_image("door", x_draw, y_draw, image_index=door_object["current_image"], centered=True)