import entities.player_functions as player_functions
import entities.entity_functions as entity_functions
import entities.background_functions as background_functions
import entities.tilemap_functions as tilemap_functions
import head_up_display


def update_camera(level_data, game_data):    
    camera_x = level_data["camera"]["x"]
    camera_y = level_data["camera"]["y"]
    camera_margin = level_data["camera"]["margin"]
    level_width = level_data["level_width"]
    level_height = level_data["level_height"]
    player_object = level_data["entities"][0]

    w = game_data["screen_width"]
    h = game_data["screen_height"]
    if player_object["x"] - camera_x < camera_margin:
        camera_x = player_object["x"] - camera_margin
    if camera_x + w - player_object["x"] < camera_margin:
        camera_x = player_object["x"] - w + camera_margin
    if player_object["y"] - camera_y < camera_margin:
        camera_y = player_object["y"] - camera_margin
    if camera_y + h - player_object["y"] < camera_margin:
        camera_y = player_object["y"] - h + camera_margin
    # la caméra ne doit jamais montrer en dehors des limites du niveau
    camera_x = max(0, camera_x)
    camera_y = max(0, camera_y)
    camera_x = min(camera_x, level_width - w)
    camera_y = min(camera_y, level_height - h)

    level_data["camera"]["x"] = camera_x
    level_data["camera"]["y"] = camera_y

def apply_message(message, level_data, game_data):
    if message["type"] == "add_entity":
        level_data["entities"].append(message["object"])
    elif message["type"] == "remove_entity":
        level_data["entities"].remove(message["object"])
    elif message["type"] == "damage_player":
        player_object = level_data["entities"][0]
        player_functions.damage_player(player_object, message["object"])
    else: 
        game_data["messages"].append(message)

def update(level_data, game_data):

    level_data["messages"] = []

    entities = level_data["entities"]
    for entity in entities:
        entity_functions.update(entity, level_data)

    # mettre à jour la caméra pour garder la joueur dans le champ visible
    update_camera(level_data, game_data)

    for message in level_data["messages"]:
        apply_message(message, level_data, game_data)

def render(level_data, game_data):
                     
    background_functions.render(level_data)

    tilemap_object = level_data["tilemap_object"]
    tilemap_functions.render(tilemap_object, level_data)                     

    entities = level_data["entities"]
    for entity in entities:
        entity_functions.render(entity, level_data)

    head_up_display.render(level_data)  