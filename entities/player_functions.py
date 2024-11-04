import pygame
import collision_functions
import entities.projectile_functions as projectile_functions
import renderer
import math

def update(player_object, game_data):
    projectile_object = game_data["projectile_object"]
    #fonction pygame qui nous permet de savoir quelles touches du clavier sont pressées en ce moment. keys[une certaine touche] sera True si cette touche est pressée, False sinon    
    keys = pygame.key.get_pressed()
    
    # les appuis sur les touches gauche et droite modifient l'angle courant du joueur.
    if keys[pygame.K_LEFT]: 
        player_object["angle"]+=5
    if keys[pygame.K_RIGHT]: 
        player_object["angle"]-=5

    # on crée un projectile si la touche espace est pressée et qu'il n'y a actuellement pas de projectile
    if keys[pygame.K_SPACE] and not projectile_object["has_projectile"] :
        projectile_functions.add_projectile(projectile_object, game_data)

    # la vitesse de déplacement du joueur en x et y est décidée selon les appuis sur les touches haut et bas et selon l'angle courant du joueur. Détail à étudier ensemble.
    if keys[pygame.K_UP]:
        player_object["vx"] = 5 * math.cos(math.radians(player_object["angle"]))
        player_object["vy"] = -5 * math.sin(math.radians(player_object["angle"]))
    elif keys[pygame.K_DOWN]: 
        player_object["vx"] = -5 * math.cos(math.radians(player_object["angle"]))
        player_object["vy"] = 5 * math.sin(math.radians(player_object["angle"]))
    else:
        player_object["vx"] = 0
        player_object["vy"] = 0
    
    # on appelle la fonction de déplacement du joueur après avoir calculé sa vitesse
    move_player(player_object, game_data)

# Cette fonction déplace le joueur à chaque frame. Deux mouvements sont effectués : un mouvement selon x et l'autre selon y.
# Dans chaque cas, si une collision est détectée après le mouvement, le mouvement est annulé et on reste dans la position actuelle.
def move_player(player_object, game_data):
    player_object = game_data["player_object"]
    tilemap_object = game_data["tilemap_object"]
    player_object["x"] += player_object["vx"]
    if collision_functions.is_collision_with_tilemap(player_object["x"], player_object["y"], player_object["hitbox"], tilemap_object):
        player_object["x"]-=player_object["vx"]
    player_object["y"] += player_object["vy"]
    if collision_functions.is_collision_with_tilemap(player_object["x"], player_object["y"], player_object["hitbox"], tilemap_object):
        player_object["y"]-=player_object["vy"]

def render(player_object, game_data):
    camera_x = game_data["camera"]["x"]
    camera_y = game_data["camera"]["y"]
    x_draw = player_object["x"] - camera_x
    y_draw = player_object["y"] - camera_y
    renderer.draw_image("player", x_draw, y_draw, centered=True, angle=player_object["angle"])