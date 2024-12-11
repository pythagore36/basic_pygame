import pygame
import io
import tkinter as tk
import entity_stuff

images = {}
font = None

selectionSurface = pygame.Surface([1500,1500])


def init():
    global font
    font = pygame.font.SysFont("arial",15)

    tiles_sheet = pygame.image.load("images/textures32.png").convert_alpha()
    image_tiles = []
    for i in range(15):
        image_tiles.append(pygame.transform.scale(tiles_sheet.subsurface(i*64,0,64,64).convert_alpha(), (32,32)))
    for i in range(8):
        image_tiles.append(pygame.transform.scale(tiles_sheet.subsurface(i*64,65,64,64).convert_alpha(), (32,32)))
    images["tiles"] = image_tiles
    
    # entities
    images["player"] = pygame.image.load("images/ship.png").convert_alpha()
    images["flag"] = pygame.transform.scale(pygame.image.load("images/flag.png").convert_alpha(),(40,40))
    images["mine"] = pygame.transform.scale(pygame.image.load("images/mine.png").convert_alpha(),(40,40))
    
    door_sprite_sheet = pygame.image.load("images/doors.png").convert_alpha()
    images["door"] = door_sprite_sheet.subsurface(15,229,64,64).convert_alpha()

    lever_sprite_sheet = pygame.image.load("images/lever.png").convert_alpha()
    images["lever"] = lever_sprite_sheet.subsurface(0,0,32,32).convert_alpha()

    images["enemy"] = pygame.image.load("images/turret.png").convert_alpha()

    return

def render_canvas(data):  
    surface = None  
    if "canvas_width" in data and "canvas_height" in data:
        surface = pygame.Surface([data["canvas_width"],data["canvas_height"]])
    else:
        surface = pygame.Surface([1500,1500])
    surface.fill('gray')
    tiles = data["tiles"]   
    entities = data["entities"] 
    pov = data["pov"]
    tile_width = data["tile_width"]
    tile_height = data["tile_height"]

    canvas_height = 400
    if "canvas_height" in data:
        canvas_height = data["canvas_height"]

    for row in range(len(tiles)):
        for col in range(len(tiles[row])):
            tile = tiles[row][col]
            x = (col - pov["x"]) * tile_width
            y = (row - pov["y"]) * tile_height
            if tile > 0:
                image = images["tiles"][tile-1]                
                surface.blit(image,(x,y))
            else:
                pygame.draw.rect(surface, "black", (x,y, tile_width, tile_height))

    if data["mode"] == "tilemap" and data["mouse_inside_canvas"] and "selected_tile" in data and "mouse_tile_x" in data and "mouse_tile_y" in data:
        tile = data["selected_tile"]
        if tile > 0:
            image = images["tiles"][tile-1]
            x = (data["mouse_tile_x"] - pov["x"]) * tile_width
            y = (data["mouse_tile_y"] - pov["y"]) * tile_height
            surface.blit(image,(x,y))

    if data["mode"] == "entities" and data["submode"] == "add_entities" and data["mouse_inside_canvas"] and "selected_entity" in data and "mouse_x" in data and "mouse_y" in data:
        entity_index = data["selected_entity"]
        image = images[entity_stuff.get_entity_data()["entities"][entity_index]["image"]]
        x = data["mouse_x"] - image.get_width()/2
        y = data["mouse_y"] - image.get_height()/2
        surface.blit(image,(x,y))

    for entity in entities:
        x = int(entity["x"]) - pov["x"] * tile_width
        y = int(entity["y"]) - pov["y"] * tile_height
        angle = 0
        if "angle" in entity:
            angle = int(entity["angle"])
        name = entity["type"]
        image = images[entity_stuff.get_image_by_entity_name(name)]
        rotated_image = pygame.transform.rotate(image,angle)    
        x = x - rotated_image.get_width()/2
        y = y - rotated_image.get_height()/2
        surface.blit(rotated_image,(x,y))

        if data["mode"] == "entities" and data["submode"] == "select_entity" and data["mouse_inside_canvas"] and "mouse_on_entity" in data and entity == data["mouse_on_entity"]:
            pygame.draw.rect(surface,"blue", (x,y, rotated_image.get_width(), rotated_image.get_height()), width=1)
        
        if entity_stuff.can_remove_by_name(entity["type"]) and data["mode"] == "entities" and data["submode"] == "remove_entity" and data["mouse_inside_canvas"] and "mouse_on_entity" in data and entity == data["mouse_on_entity"]:            
            pygame.draw.line(surface, "red", (x,y), (x + rotated_image.get_width(), y + rotated_image.get_height()))
            pygame.draw.line(surface, "red", (x,y + rotated_image.get_height()), (x + rotated_image.get_width(), y))

        if data["mode"] == "entities" and data["submode"] == "select_entity" and "current_selected_entity" in data and entity == data["current_selected_entity"]:
            pygame.draw.rect(surface,"red", (x,y, rotated_image.get_width(), rotated_image.get_height()), width=1)

    coordinate_text_surface = font.render(data["text_coordinates"], True, "white")
    text_x = 20
    text_y = canvas_height - 20 
    
    surface.blit(coordinate_text_surface, (text_x, text_y))


    fileobj = io.BytesIO()

    pygame.image.save(surface, fileobj, "test.png")

    photo_image = tk.PhotoImage(data=fileobj.getbuffer().tobytes())

    fileobj.close()

    return photo_image

def render_selection_canvas(data):
    selectionSurface.fill((0, 0, 0))



    tile_width = data["tile_width"]
    tile_height = data["tile_height"]
    first_element = data["selection_first_element"]
    last_element = data["selection_last_element"]

    if data["mode"] == "tilemap":
        for tile in range(first_element, last_element+1):
            x = (tile - first_element) * tile_width
            y = 20        
            if tile == 0:
                pygame.draw.rect(selectionSurface, "gray75", (x,y, tile_width, tile_height))            
                pygame.draw.line(selectionSurface, "red", (x,y), (x + tile_width, y + tile_height))
                pygame.draw.line(selectionSurface, "red", (x,y + tile_height), (x + tile_width, y))
            else:
                image = images["tiles"][tile-1]                
                selectionSurface.blit(image,(x,y))
            if "selected_tile" in data and tile == data["selected_tile"]:
                pygame.draw.rect(selectionSurface,"blue", (x,y, tile_width, tile_height), width=1)
    
    elif data["mode"] == "entities" and data["submode"] == "add_entities":
        entity_width = entity_stuff.get_entity_data()["image_width"]
        entity_height = entity_stuff.get_entity_data()["image_height"]
        for entity in range(first_element, last_element + 1):
            x = (entity - first_element) * entity_width
            y = 20
            image = pygame.transform.scale(images[entity_stuff.get_entity_data()["entities"][entity]["image"]],(entity_width, entity_height))
            selectionSurface.blit(image,(x,y))
            if "selected_entity" in data and entity == data["selected_entity"]:
                pygame.draw.rect(selectionSurface,"blue", (x,y, entity_width, entity_height), width=1)

    fileobj = io.BytesIO()

    pygame.image.save(selectionSurface, fileobj, "test.png")

    photo_image = tk.PhotoImage(data=fileobj.getbuffer().tobytes())

    fileobj.close()

    return photo_image