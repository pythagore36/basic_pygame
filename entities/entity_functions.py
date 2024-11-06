import entities.player_functions as player_functions
import entities.projectile_functions as projectile_functions
import entities.mine_functions as mine_functions
import entities.flag_functions as flag_functions

def update(entity, game_data):
    if entity["type"] == "player":
        player_functions.update(entity, game_data)
    elif entity["type"] == "projectile":
        projectile_functions.update(entity, game_data)
    elif entity["type"] == "mine":
        mine_functions.update(entity, game_data)
    elif entity["type"] == "flag":
        flag_functions.update(entity, game_data)

def render(entity, game_data):
    if entity["type"] == "player":
        player_functions.render(entity, game_data)
    elif entity["type"] == "projectile":
        projectile_functions.render(entity, game_data)
    elif entity["type"] == "mine":
        mine_functions.render(entity, game_data)
    elif entity["type"] == "flag":
        flag_functions.render(entity, game_data)