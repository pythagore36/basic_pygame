import pygame
import game_functions
import renderer

game_data = game_functions.init_game_data()

renderer.init(game_data)        

# un objet pygame qui nous permet de fixer le nombre de frames executées par seconde, pour que le jeu tourne toujours à la même vitesse.
clock=pygame.time.Clock()

# début de la boucle principale du jeu
while game_data["running"]:
    # retarder un petit peu selon un délai calculé de façon à ce qu'on passe exactement 60 fois dans la boucle en une seconde.
    clock.tick(60)
    # si l'utilisateur clique sur la croix, on met running à False pour sortir de la boucle 
    for event in pygame.event.get(): 
        if event.type == pygame.QUIT: 
            game_data["running"] = False    
    # mettre à jour l'état du jeu
    game_functions.update(game_data)
    # redessiner l'état du jeu dans la fenêtre.
    game_functions.render(game_data)

# fonction pygame qu'il faut appeler à la fin du programme pour quitter correctement.
pygame.quit()