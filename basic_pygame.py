import pygame
import math

# initialisation de pygame, obligatoire à faire avant d'utiliser n'importe quoi d'autre
pygame.init()

# screen_window est une Surface correspondant directement à la fenêtre qui s'affiche sur l'écran
screen_window = pygame.display.set_mode((600, 600),pygame.RESIZABLE)

# nom de la fenêtre
pygame.display.set_caption("Test")

# game_surface est une Surface sur laquelle on dessine un par un tous les objets du jeu. Quand on veut mettre à jour l'affichage de l'écran, on "colle" (blit) game_surface sur screen_window.
game_surface=pygame.Surface([608, 608])

#camera
camera_x = 0
camera_y = 0
camera_margin = 200

# ------------ informations du joueur -------------------
# coordonnées x et y de la position du joueur
player_x = 300
player_y = 300
# vitesse courante du joueur selon x et y. Le principe est que s'il n'y a pas d'obstacle, à la prochaine mise à jour de la position du joueur, les coordonnées x et y du joueur augmentent de vx et vy.
vx = 0
vy = 0
# angle courant du joueur.
angle = 0
# la partie solide du joueur dont on testera la collision avec les murs. C'est un rectangle qui se déplace avec le joueur dont le coin supérieur gauche à pour coordonnées :
# x = player_x + player_hitbox_x
# y = player_y + player_hitbox_y
# et dont la longueur vaut player_hitbox_width et la hauteur vaut player_hitbox_height
player_hitbox_x=-15
player_hitbox_y=-15
player_hitbox_width=30
player_hitbox_height=30

# ------------ informations du projectile -------------------
# informations similaires à celles du joueur définies plus haut. La position et vitesse sont juste initialisées à 0. Leurs valeurs sont décidées au moment où on "crée" un projectile
projectile_angle = 0
projectile_x = 0
projectile_y = 0
projectile_vx = 0
projectile_vy = 0
projectile_hitbox_x=-15
projectile_hitbox_y=-15
projectile_hitbox_width=30
projectile_hitbox_height=30

# True s'il y a un projectile en ce moment, False sinon
has_projectile = False

# le projectile peut être dans un des deux états : "moving" ou "exploding".
projectile_state = 'moving'

# si le projectile est "moving" depuis cette durée, il passe à "exploding"
moving_timer = 120

# depuis combien de temps le projectile est "exploding"
explosion_timer = 0

# combien de frames on reste sur chaque image de l'explosion avant de passer à la suivante
delay = 3

# ------------ informations du tilemap -------------------
# le tilemap permet de placer les obstacles solides (les murs) du niveau. C'est une grille rectangulaire.

# nombre de colonnes du tilemap
tile_map_width = 40

# nombre de lignes du tilemap. Le nombre de cases (tiles) dans le tilemap est donc tile_map_width * tile_map_height
tile_map_height = 40

# longueur en pixels d'une case du tilemap. La longueur en pixels du niveau est donc tile_map_width * tile_width
tile_width = 32

# hauteur en pixels d'une case du tilemap. La hauteur en pixels du niveau est donc tile_map_height * tile_height
tile_height = 32

# le tilemap lui même en un seul grand tableau. Les 1 sont des tiles solides, les 0 sont des tiles vides.
# Pour accéder au tile situé ligne i - colonne j on fait tile_map[i * tile_map_width + j]
# Si on veut connaitre la ligne et la colonne d'une tile n, on fait :
# ligne = int(n / tile_map_width). C'est le quotient dans la division du numéro de la tile par le nombre de colonnes du tilemap
# colonne = n % tile_map_width. C'est le reste dans la même division.
tile_map = [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,
            1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,
            1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,
            1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,
            1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,
            1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,
            1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,
            1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,
            1,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,
            1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,4,4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,
            1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,
            1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,
            1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,4,4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,
            1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,
            1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,
            1,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,
            1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,
            1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,
            1,1,1,1,1,1,1,1,1,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,
            1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,
            1,1,1,1,1,1,1,1,1,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,
            1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,
            1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,
            1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,
            1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,
            1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,
            1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,
            1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,
            1,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,
            1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,4,4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,
            1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,
            1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,
            1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,4,4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,
            1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,
            1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,
            1,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,
            1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,
            1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,
            1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,
            1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]

# utiliser des fonctions pygame pour charger des images à partir des fichiers sur le disque. Le résultat de la fonction est une Surface sur laquelle on peut ensuite appliquer 
# des transformations telles que la rotation ou le scaling. On peut "coller" (blit) ces objets Surface sur une autre Surface.
image_player = pygame.image.load("ship.png").convert_alpha()
image_fireball = pygame.image.load("fireball.png").convert_alpha()

# on charge une image qu'on découpe ensuite en plusieurs petite images qui sont les différentes images de l'animation d'explosion. Les images sont mises dans le tableau image_explosions.
explosion_sprite_sheet = pygame.image.load("explosion_sprites.png").convert_alpha()
image_explosions = []
for i in range(13):
    image_explosions.append(explosion_sprite_sheet.subsurface(i*39,117,39,39).convert_alpha())

tiles_sheet = pygame.image.load("textures32.png").convert_alpha()
image_tiles = []
for i in range(15):
    image_tiles.append(pygame.transform.scale(tiles_sheet.subsurface(i*64,0,64,64).convert_alpha(), (32,32)))
for i in range(8):
    image_tiles.append(pygame.transform.scale(tiles_sheet.subsurface(i*64,65,64,64).convert_alpha(), (32,32)))


# cette fonction prend en entrée les coordonnées x et y d'un objet du jeu (soit le joueur, soit le projectile), ainsi que les informations sur la "zone solide" (hitbox) de cet objet.
# On retourne True si la "zone solide" de l'objet est en contact avec une tile solide du tilemap, False sinon.
# En clair, ça nous dit si on est à l'intérieur d'un mur.
# Contenu de la fonction à étudier ensemble.
def is_collision(x, y, hitbox_x, hitbox_y, hitbox_width, hitbox_height):
    hitbox_x1 = x + hitbox_x
    hitbox_y1 = y + hitbox_y
    hitbox_x2 = hitbox_x1 + hitbox_width
    hitbox_y2 = hitbox_y1 + hitbox_height

    row1 = int(hitbox_y1 / tile_height)
    col1 = int(hitbox_x1 / tile_width)
    row2 = int(hitbox_y2 / tile_height)
    col2 = int(hitbox_x2 / tile_width)

    for row in range(row1, row2+1):
        for col in range(col1, col2+1):
            tile_position = row * tile_map_width + col
            if tile_position >= 0 and tile_position < len(tile_map) and tile_map[tile_position] != 0:
                return True
    return False


# fonction qui supprime le projectile à la fin de l'animation d'explosion. Il suffit de mettre le boolean has_projectile à False
def remove_projectile():
    global has_projectile
    has_projectile = False

# fonction qui crée un projectile depuis l'emplacement courant du joueur et avec l'angle courant du joueur. Contenu de la fonction à étudier ensemble.
def add_projectile():
    global has_projectile, projectile_state, projectile_vx, projectile_vy, projectile_x, projectile_y, moving_timer, projectile_angle
    has_projectile = True
    direction_x = math.cos(math.radians(angle))
    direction_y = -math.sin(math.radians(angle))
    projectile_x = player_x + direction_x * 10
    projectile_y = player_y + direction_y * 10
    projectile_state = 'moving'
    projectile_angle = angle
    moving_timer = 300
    projectile_vx = direction_x * 10
    projectile_vy = direction_y * 10

# fonction qui met à jour le projectile  à chaque frame s'il existe
def update_projectile():
    global explosion_timer, moving_timer, projectile_state, projectile_x, projectile_y
    # si le projectile est à l'état "moving" il continue d'avance selon sa vitesse en x et en y.
    if projectile_state == 'moving':
        projectile_x += projectile_vx
        projectile_y += projectile_vy
        moving_timer -= 1
        # si le projectile est arrivé à la fin de sa durée de vie ou qu'il a touché un obstacle solide, il passe en mode "exploding"
        if moving_timer <= 0 or is_collision(projectile_x, projectile_y, projectile_hitbox_x, projectile_hitbox_y, projectile_hitbox_width, projectile_hitbox_height):
            projectile_state = 'exploding'
            explosion_timer = 0            
    # si le projectile est en mode "exploding", on augmente le timer de l'explosion  pour qu'on sache à quelle image on en est.
    elif projectile_state == 'exploding':
        explosion_timer += 1
        # si on est arrivé à la fin de l'animation d'explosion, on supprime le projectile
        if explosion_timer > delay * len(image_explosions):
            remove_projectile()

# cette fonction retourne l'image qu'il faut actuellemet afficher pour le projectile.
def image_projectile():
    # si le projectile est "moving" on renvoie son image normale, après transformation par rotation selon l'angle du projectile.
    if projectile_state == 'moving':
        return pygame.transform.rotate(image_fireball,projectile_angle)
    # sinon le projectile est "exploding". On renvoie l'une des images du tableau image_explosions, selon le timer de l'explosion.
    i = int(explosion_timer / delay) % len(image_explosions)
    return image_explosions[i]


# Cette fonction déplace le joueur à chaque frame. Deux mouvements sont effectués : un mouvement selon x et l'autre selon y.
# Dans chaque cas, si une collision est détectée après le mouvement, le mouvement est annulé et on reste dans la position actuelle.
def move_player():
    global player_x, player_y
    player_x += vx
    if is_collision(player_x, player_y, player_hitbox_x, player_hitbox_y, player_hitbox_width, player_hitbox_height):
        player_x-=vx
    player_y += vy
    if is_collision(player_x, player_y, player_hitbox_x, player_hitbox_y, player_hitbox_width, player_hitbox_height):
        player_y-=vy

def update_camera():    
    global camera_x, camera_y
    (w,h) = game_surface.get_size()
    if player_x - camera_x < camera_margin:
        camera_x = player_x - camera_margin
    if camera_x + w - player_x < camera_margin:
        camera_x = player_x - w + camera_margin
    if player_y - camera_y < camera_margin:
        camera_y = player_y - camera_margin
    if camera_y + h - player_y < camera_margin:
        camera_y = player_y - h + camera_margin 


# cette fonction met à jour l'état du jeu à chaque frame.
def update_game():
    global vx, vy, angle
    #fonction pygame qui nous permet de savoir quelles touches du clavier sont pressées en ce moment. keys[une certaine touche] sera True si cette touche est pressée, False sinon    
    keys = pygame.key.get_pressed()
    
    # les appuis sur les touches gauche et droite modifient l'angle courant du joueur.
    if keys[pygame.K_LEFT]: 
        angle+=5
    if keys[pygame.K_RIGHT]: 
        angle-=5

    # on crée un projectile si la touche espace est pressée et qu'il n'y a actuellement pas de projectile
    if keys[pygame.K_SPACE] and not has_projectile:
        add_projectile()

    # la vitesse de déplacement du joueur en x et y est décidée selon les appuis sur les touches haut et bas et selon l'angle courant du joueur. Détail à étudier ensemble.
    if keys[pygame.K_UP]:
        vx = 5 * math.cos(math.radians(angle))
        vy = -5 * math.sin(math.radians(angle))
    elif keys[pygame.K_DOWN]: 
        vx = -5 * math.cos(math.radians(angle))
        vy = 5 * math.sin(math.radians(angle))
    else:
        vx = 0
        vy = 0
    
    # on appelle la fonction de déplacement du joueur après avoir calculé sa vitesse
    move_player()

    # mettre à jour la caméra pour garder la joueur dans le champ visible
    update_camera()

    # s'il y a un projectile, on le met à jour.
    if has_projectile:
        update_projectile()

# cette fonction redessine l'écran à chaque frame.
# On dessine tout ce qu'il y a à dessiner sur la Surface game_surface. Quand game_surface est prête, on la colle sur la Surface screen_window pour l'afficher dans notre fenêtre de jeu.
def render_screen():
    # on commence par reset le game_surface en la remplissant avec un fonc noir pour effacer tout ce qu'il y avait à la frame précédente. Dans une prochaine version, on pourrait
    # essayer de mettre une image de background à la place.
    game_surface.fill((0, 0, 0))

    # on dessine le tilemap ligne par ligne. Pour chaque ligne, on prend les colonnes une à une, on regarde la tile présente à cet endroit. Si on trouve 1, on calcule les coordonnées
    # x et y de la tile sur l'écran et on "blit" l'image de la tile à ces coordonnées sur la game_surface
    for row in range(tile_map_height):
        for col in range(tile_map_width):
            tile_position = row * tile_map_width + col
            tile = tile_map[tile_position]
            if tile > 0 and tile < len(image_tiles):
                x_tile = col * tile_width - camera_x
                y_tile = row * tile_height - camera_y
                game_surface.blit(image_tiles[tile - 1], (x_tile, y_tile))


    # on dessine le joueur. On transforme l'image du joueur par une rotation selon l'angle courant du joueur. 
    # On calcule les coordonnées x et y de l'image de façon à ce que les coordonnées x et y du joueur correspondent au centre de l'image.
    image_angle = pygame.transform.rotate(image_player,angle)
    x_draw = player_x - image_angle.get_width()/2 - camera_x
    y_draw = player_y - image_angle.get_height()/2 - camera_y
    game_surface.blit(image_angle,(x_draw,y_draw))

    # enfin on dessine le projectile s'il y en a un. On utilise la fonction définie avant pour utiliser la bonne image.
    # Comme pour le joueur, les coordonnées x et y du projectile corresponent au centre de l'image affichée.
    if has_projectile:
        image = image_projectile()
        x_draw = projectile_x - image.get_width()/2 - camera_x
        y_draw = projectile_y - image.get_height()/2 - camera_y
        game_surface.blit(image,(x_draw,y_draw))

    # maintenant la game_surface est prête, il nous reste à la copier dans screen_window qui est la Surface qu'on affiche à l'écran.
    # Depuis le début du programme, la taille de game_surface reste toujours la même. Par contre le screen_window peut changer de taille 
    # si l'utilisateur agrandit la taille de la fenêtre sous Windows par exemple. On veut donc "scale" la taille de la game_surface pour que ça remplisse exactement la screen_window.

    # une fonction pygame pour obtenir la taille actuelle de la fenêtre windows que l'utilisateur a peut être modifié.
    screen_size=screen_window.get_size()

    # une fonction pygame pour "scale" la game surface selon screen_size et "blit" le résultat dans screen_window. Après ça le screen_window contient
    # l'image qui doit être affichée à l'utilisateur
    pygame.transform.scale(game_surface,screen_size, screen_window)   

    # une fonction pygame qui met à jour l'affichage Windows pour qu'on voit dans la fenêtre le contenu de screen_window
    pygame.display.update()


# le programme principal s'execute ici. Pour un jeu, on ne veut pas que le programme termine tant que l'utilisateur n'a pas choisi de quitter. Donc on se met dans une boucle "infinie".
# Chaque passage dans la boucle est appelé une frame. C'est l'unité la plus petite d'avancement des actions du jeu.

# tant que running est vrai on continue l'execution du programme
running = True

# un objet pygame qui nous permet de fixer le nombre de frames executées par seconde, pour que le jeu tourne toujours à la même vitesse.
clock=pygame.time.Clock()

# début de la boucle principale du jeu
while running:
    # retarder un petit peu selon un délai calculé de façon à ce qu'on passe exactement 60 fois dans la boucle en une seconde.
    clock.tick(60)
    # si l'utilisateur clique sur la croix, on met running à False pour sortir de la boucle 
    for event in pygame.event.get(): 
        if event.type == pygame.QUIT: 
            running = False    
    # mettre à jour l'état du jeu
    update_game()
    # redessiner l'état du jeu dans la fenêtre.
    render_screen()

# fonction pygame qu'il faut appeler à la fin du programme pour quitter correctement.
pygame.quit()

# juste afficher un truc dans la console pour vérifier qu'on a bien quitté la boucle correctement.
print("thank you for playing")