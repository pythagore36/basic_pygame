import pygame
import image_manager

renderer_object = {}

def init(game_data):
    pygame.init()
    pygame.font.init()

    renderer_object["font_big"] = pygame.font.SysFont("arial",40)
    renderer_object["font_middle"] = pygame.font.SysFont("arial",30)
    renderer_object["screen_window"] = pygame.display.set_mode((600, 600),pygame.RESIZABLE)
    screen_width = game_data["screen_width"]
    screen_height = game_data["screen_height"]
    renderer_object["game_surface"] = pygame.Surface([screen_width, screen_height])

    pygame.display.set_caption("Basic Pygame")

    image_manager.init(game_data)

def init_frame():    
    renderer_object["game_surface"].fill((0, 0, 0))

def write_text_big(text, y):
    font = renderer_object["font_big"]
    write_text(text,y,font)

def write_text_middle(text, y):
    font = renderer_object["font_middle"]
    write_text(text,y,font)

def write_text(text, y, font):
    game_surface = renderer_object["game_surface"]
    text_surface = font.render(text, True, "white")
    text_x = game_surface.get_width()/2 - text_surface.get_width()/2    
    
    game_surface.blit(text_surface, (text_x, y))

def draw_image(image_key, x, y, image_index=-1, centered = False, angle = 0):
    game_surface = renderer_object["game_surface"]
    image = image_manager.getImage(image_key, image_index)
    rotated_image = pygame.transform.rotate(image,angle)
    if centered:
        x = x - rotated_image.get_width()/2
        y = y - rotated_image.get_height()/2
    game_surface.blit(rotated_image,(x,y)) 

def refresh_screen():
    game_surface = renderer_object["game_surface"]
    screen_window = renderer_object["screen_window"]
    screen_size=screen_window.get_size()    
    pygame.transform.scale(game_surface,screen_size, screen_window)       
    pygame.display.update()

def get_animation_length(animation_key):
    return image_manager.getLength(animation_key)