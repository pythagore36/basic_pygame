import pygame
import math
import sat_collision

pygame.init()

screen_window = pygame.display.set_mode((608, 608),pygame.RESIZABLE)
game_surface = pygame.Surface([608, 608])

pygame.display.set_caption("Collision testing")

polygon_1 = {
    "x" : 100,
    "y" : 100,
    "color" : "red",
    "angle" : 0,
    "points" : [(-40, -30),(5,-60),(34, 30)]
}

polygon_2 = {
    "x" : 500,
    "y" : 150,
    "color" : "green",
    "angle" : 0,
    "points" : [(-20, -40),(10,-24),(50, 36),(-50, 36)]
}

polygons = [polygon_1, polygon_2]

def update():
    global polygon_1, polygon_2

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        polygon_1["x"] -= 5
    if keys[pygame.K_RIGHT]:
        polygon_1["x"] += 5
    if keys[pygame.K_UP]:
        polygon_1["y"] -= 5
    if keys[pygame.K_DOWN]:
        polygon_1["y"] += 5
    if keys[pygame.K_k]:
        polygon_1["angle"] += 5
    if keys[pygame.K_l]:
        polygon_1["angle"] -= 5

    if keys[pygame.K_q]:
        polygon_2["x"] -= 5
    if keys[pygame.K_d]:
        polygon_2["x"] += 5
    if keys[pygame.K_z]:
        polygon_2["y"] -= 5
    if keys[pygame.K_s]:
        polygon_2["y"] += 5
    if keys[pygame.K_a]:
        polygon_2["angle"] += 5
    if keys[pygame.K_e]:
        polygon_2["angle"] -= 5

def transform(point, polygon):

    angle = math.radians(polygon["angle"])
    rotated_point = (point[0] * math.cos(angle) + point[1] * math.sin(angle),
                     point[1] * math.cos(angle) - point[0] * math.sin(angle))

    return (polygon["x"] + rotated_point[0], polygon["y"] + rotated_point[1])

def test_collision(points_1, points_2):
    return sat_collision.polygon_to_polygon(points_1, points_2)

def render():
    global game_surface, screen_window
    game_surface.fill((0,0,0))

    for polygon in polygons:
        points = []
        for point in polygon["points"]:
            points.append(transform(point, polygon))
        pygame.draw.polygon(game_surface, polygon["color"], points)
        pygame.draw.rect(game_surface, "black", 
                         (polygon["x"]-1,polygon["y"]-1,2,2))

        points_1 = []
        for point in polygon_1["points"]:
            points_1.append(transform(point, polygon_1))
        
        points_2 = []
        for point in polygon_2["points"]:
            points_2.append(transform(point, polygon_2))
        
        if test_collision(points_1, points_2):
            pygame.draw.circle(game_surface, "red", (550,550), 30)
        else:
            pygame.draw.circle(game_surface, "green", (550,550), 30)

    screen_size=screen_window.get_size()   
    pygame.transform.scale(game_surface,screen_size, screen_window)       
    pygame.display.update()


clock=pygame.time.Clock()

def run():

    running = True

    while running:    
        clock.tick(60)    
        for event in pygame.event.get(): 
            if event.type == pygame.QUIT: 
                running = False    
        update()
        render()


    pygame.quit()