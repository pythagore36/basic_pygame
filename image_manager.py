import pygame

images = {}

def init(game_data):
    global images
    images["player"] = pygame.image.load("images/ship.png").convert_alpha()
    images["fireball"] = pygame.image.load("images/fireball.png").convert_alpha()
    images["flag"] = pygame.transform.scale(pygame.image.load("images/flag.png").convert_alpha(),(40,40))
    images["mine"] = pygame.transform.scale(pygame.image.load("images/mine.png").convert_alpha(),(40,40))
    images["background"] = pygame.transform.scale(pygame.image.load("images/background.jpg").convert_alpha(), (974,608))

    explosion_sprite_sheet = pygame.image.load("images/explosion_sprites.png").convert_alpha()
    image_explosions = []
    for i in range(13):
        image_explosions.append(explosion_sprite_sheet.subsurface(i*39,117,39,39).convert_alpha())
    images["explosion"] = image_explosions

    door_sprite_sheet = pygame.image.load("images/doors.png").convert_alpha()
    image_door = []
    for i in range(7):
        image_door.append(door_sprite_sheet.subsurface(15 + i*64,229,64,64).convert_alpha())
    images["door"] = image_door

    lever_sprite_sheet = pygame.image.load("images/lever.png").convert_alpha()
    image_lever = []
    image_lever.append(lever_sprite_sheet.subsurface(0,0,32,32).convert_alpha())
    image_lever.append(lever_sprite_sheet.subsurface(0,64,32,32).convert_alpha())
    images["lever"] = image_lever

    tiles_sheet = pygame.image.load("images/textures32.png").convert_alpha()
    image_tiles = []
    for i in range(15):
        image_tiles.append(pygame.transform.scale(tiles_sheet.subsurface(i*64,0,64,64).convert_alpha(), (32,32)))
    for i in range(8):
        image_tiles.append(pygame.transform.scale(tiles_sheet.subsurface(i*64,65,64,64).convert_alpha(), (32,32)))
    images["tiles"] = image_tiles

    images["heart"] = pygame.transform.scale(pygame.image.load("images/heart.png").convert_alpha(),(40,40))

    images["turret"] = pygame.image.load("images/turret.png").convert_alpha()

def load_sprite(sprite):
    global images
    if not "path" in sprite or not "key" in sprite:
        return
    path = sprite["path"]
    key = sprite["key"]
    image = pygame.image.load(path).convert_alpha()
    x = 0
    if "x" in sprite:
        x = int(sprite["x"])
    y = 0
    if "y" in sprite:
        y = int(sprite["y"])
    number_of_images = 1
    if "number_of_images" in sprite:
        number_of_images = int(sprite["number_of_images"])
    width_origin = image.get_width()
    if "width_origin" in sprite:
        width_origin = int(sprite["width_origin"])
    height_origin = image.get_height()
    if "height_origin" in sprite:
        height_origin = int(sprite["height_origin"])
    images_per_row = 1
    if "images_per_row" in sprite:
        images_per_row = int(sprite["images_per_row"])
    width_game = width_origin
    if "width_game" in sprite:
        width_game = int(sprite["width_game"])
    height_game = height_origin
    if "height_game" in sprite:
        height_game = int(sprite["height_game"])
    if number_of_images == 1:
        images[key] = pygame.transform.scale(image.subsurface(x,y,width_origin,height_origin).convert_alpha(), (width_game,height_game))
    else:
        for i in range(number_of_images):
            row = int(i / images_per_row)
            col = i % images_per_row
            images[key+str(i)] = pygame.transform.scale(image.subsurface(x + col * width_origin,y + row * height_origin,width_origin,height_origin).convert_alpha(), (width_game,height_game))

def getImage(key, index = -1):
    if index == -1:
        return images[key]
    return images[key][index]

def getLength(key):
    return len(images[key])

def get_image_size(key, index = -1):
    image = getImage(key,index)
    return image.get_size()