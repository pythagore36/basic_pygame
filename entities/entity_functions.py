import entities.player_functions as player_functions
import entities.projectile_functions as projectile_functions
import entities.mine_functions as mine_functions
import entities.flag_functions as flag_functions
import entities.door_functions as door_functions

def update(entity, level_data):
    if entity["type"] == "player":
        player_functions.update(entity, level_data)
    elif entity["type"] == "projectile":
        projectile_functions.update(entity, level_data)
    elif entity["type"] == "mine":
        mine_functions.update(entity, level_data)
    elif entity["type"] == "flag":
        flag_functions.update(entity, level_data)
    elif entity["type"] == "door":
        door_functions.update(entity, level_data)

def render(entity, level_data):
    if entity["type"] == "player":
        player_functions.render(entity, level_data)
    elif entity["type"] == "projectile":
        projectile_functions.render(entity, level_data)
    elif entity["type"] == "mine":
        mine_functions.render(entity, level_data)
    elif entity["type"] == "flag":
        flag_functions.render(entity, level_data)
    elif entity["type"] == "door":
        door_functions.render(entity, level_data)