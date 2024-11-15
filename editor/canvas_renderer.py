import pygame
import io
import tkinter as tk

images = {}
surface = pygame.Surface([1500,1500])
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
    return

def render_canvas(data):
    surface.fill('gray')
    tiles = data["tiles"]
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

    if data["mouse_inside_canvas"] and "selected_tile" in data and "mouse_tile_x" in data and "mouse_tile_y" in data:
        tile = data["selected_tile"]
        if tile > 0:
            image = images["tiles"][tile-1]
            x = (data["mouse_tile_x"] - pov["x"]) * tile_width
            y = (data["mouse_tile_y"] - pov["y"]) * tile_height
            surface.blit(image,(x,y))

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
    first_tile = data["selection_first_tile"]
    last_tile = data["selection_last_tile"]

    for tile in range(first_tile, last_tile+1):
        x = (tile - first_tile) * tile_width
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
    
    fileobj = io.BytesIO()

    pygame.image.save(selectionSurface, fileobj, "test.png")

    photo_image = tk.PhotoImage(data=fileobj.getbuffer().tobytes())

    fileobj.close()

    return photo_image