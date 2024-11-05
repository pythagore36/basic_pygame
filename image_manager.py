import pygame

images = {}

def init(game_data):
    global images
    images["player"] = pygame.image.load("images/ship.png").convert_alpha()
    images["fireball"] = pygame.image.load("images/fireball.png").convert_alpha()
    images["flag"] = pygame.transform.scale(pygame.image.load("images/green_flag.png").convert_alpha(),(40,40))
    images["mine"] = pygame.transform.scale(pygame.image.load("images/mine.png").convert_alpha(),(40,40))
    images["background"] = pygame.transform.scale(pygame.image.load("images/background.jpg").convert_alpha(),(game_data["level_width"], game_data["level_height"]))

    explosion_sprite_sheet = pygame.image.load("images/explosion_sprites.png").convert_alpha()
    image_explosions = []
    for i in range(13):
        image_explosions.append(explosion_sprite_sheet.subsurface(i*39,117,39,39).convert_alpha())
    images["explosion"] = image_explosions

    tiles_sheet = pygame.image.load("images/textures32.png").convert_alpha()
    image_tiles = []
    for i in range(15):
        image_tiles.append(pygame.transform.scale(tiles_sheet.subsurface(i*64,0,64,64).convert_alpha(), (32,32)))
    for i in range(8):
        image_tiles.append(pygame.transform.scale(tiles_sheet.subsurface(i*64,65,64,64).convert_alpha(), (32,32)))
    images["tiles"] = image_tiles

    images["heart"] = pygame.transform.scale(pygame.image.load("images/heart.png").convert_alpha(),(40,40))

def getImage(key, index = -1):
    if index == -1:
        return images[key]
    return images[key][index]

def getLength(key):
    return len(images[key])