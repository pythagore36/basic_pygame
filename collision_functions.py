# cette fonction prend en entrée les coordonnées x et y d'un objet du jeu (soit le joueur, soit le projectile), ainsi que les informations sur la "zone solide" (hitbox) de cet objet.
# On retourne True si la "zone solide" de l'objet est en contact avec une tile solide du tilemap, False sinon.
# En clair, ça nous dit si on est à l'intérieur d'un mur.
# Contenu de la fonction à étudier ensemble.
def is_collision_with_tilemap(x, y, hitbox, tilemap):
    hitbox_x1 = x + hitbox["x"]
    hitbox_y1 = y + hitbox["y"]
    hitbox_x2 = hitbox_x1 + hitbox["width"]
    hitbox_y2 = hitbox_y1 + hitbox["height"]

    row1 = int(hitbox_y1 / tilemap["tile_height"])
    col1 = int(hitbox_x1 / tilemap["tile_width"])
    row2 = int(hitbox_y2 / tilemap["tile_height"])
    col2 = int(hitbox_x2 / tilemap["tile_width"])

    for row in range(row1, row2+1):
        for col in range(col1, col2+1):
            tile_position = row * tilemap["tile_map_width"] + col
            if tile_position >= 0 and tile_position < len(tilemap["tiles"]) and tilemap["tiles"][tile_position] != 0:
                return True
    return False

# collision entre deux objets pour lesquels on fournit les coordonnées et les informations de hitbox
def is_collision(object1_x,object1_y,object1_hitbox,
                 object2_x,object2_y,object2_hitbox):
    x1 = object1_x + object1_hitbox["x"]
    y1 = object1_y + object1_hitbox["y"]
    x2 = object2_x + object2_hitbox["x"]
    y2 = object2_y + object2_hitbox["y"]
    if x2 > x1 + object1_hitbox["width"] or x1 > x2 + object2_hitbox["width"] or y2 > y1 + object1_hitbox["height"] or y1 > y2 + object2_hitbox["height"]:
        return False
    return True

# retourne toutes les entity en collision avec l'entity donnée en argument
def collisions(entity, game_data):
    if "hitbox" not in entity:
        return []
    entities = game_data["entities"]
    result = []
    for entity_test in entities:
        if entity_test == entity or "hitbox" not in entity_test:
            continue
        if is_collision(entity["x"], entity["y"], entity["hitbox"],entity_test["x"], entity_test["y"], entity_test["hitbox"]):
            result.append(entity_test)
    return result