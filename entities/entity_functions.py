import entities.player_functions as player_functions
import entities.projectile_functions as projectile_functions
import entities.mine_functions as mine_functions
import entities.flag_functions as flag_functions
import entities.door_functions as door_functions
import entities.lever_functions as lever_functions
import entities.enemy_functions as enemy_functions
import entities.projectile_functions as projectile_functions

def init(entity):
    if entity["type"] == "player":
        player_functions.init(entity)
    if entity["type"] == "flag":
        flag_functions.init(entity)
    if entity["type"] == "door":
        door_functions.init(entity)
    if entity["type"] == "mine":
        mine_functions.init(entity)
    if entity["type"] == "projectile":
        projectile_functions.init(entity)
    if entity["type"] == "enemy":
        enemy_functions.init(entity)


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
    elif entity["type"] == "lever":
        lever_functions.update(entity, level_data)
    elif entity["type"] == "enemy":
        enemy_functions.update(entity, level_data)

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
    elif entity["type"] == "lever":
        lever_functions.render(entity, level_data)
    elif entity["type"] == "enemy":
        enemy_functions.render(entity, level_data)