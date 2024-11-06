import entities.player_functions as player_functions
import entities.entity_functions as entity_functions
import entities.background_functions as background_functions
import entities.tilemap_functions as tilemap_functions
import head_up_display


def update_camera(game_data):    
    camera_x = game_data["camera"]["x"]
    camera_y = game_data["camera"]["y"]
    camera_margin = game_data["camera"]["margin"]
    level_width = game_data["level_width"]
    level_height = game_data["level_height"]
    player_object = game_data["entities"][0]

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

    game_data["camera"]["x"] = camera_x
    game_data["camera"]["y"] = camera_y

def apply_message(message, game_data):
    if message["type"] == "add_entity":
        game_data["entities"].append(message["object"])
    elif message["type"] == "remove_entity":
        game_data["entities"].remove(message["object"])
    elif message["type"] == "damage_player":
        player_object = game_data["entities"][0]
        player_functions.damage_player(player_object, message["object"])

def update(game_data):

    game_data["messages"] = []

    entities = game_data["entities"]
    for entity in entities:
        entity_functions.update(entity, game_data)

    # mettre à jour la caméra pour garder la joueur dans le champ visible
    update_camera(game_data)

    for message in game_data["messages"]:
        apply_message(message, game_data)

def render(game_data):
                     
    background_functions.render(game_data)

    tilemap_object = game_data["tilemap_object"]
    tilemap_functions.render(tilemap_object, game_data)                     

    entities = game_data["entities"]
    for entity in entities:
        entity_functions.render(entity, game_data)

    head_up_display.render(game_data)  