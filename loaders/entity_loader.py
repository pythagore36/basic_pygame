import loaders.player_loader as player_loader
import loaders.mine_loader as mine_loader
import loaders.flag_loader as flag_loader
import loaders.door_loader as door_loader
import loaders.lever_loader as lever_loader
import loaders.enemy_loader as enemy_loader
import loaders.model_loader as model_loader
import loaders.projectile_loader as projectile_loader

import entities.entity_functions as entity_functions

def load_entity(entity_data):
    entity_type = entity_data["type"]
    entity = None
    if entity_type == "player":
        entity =  player_loader.load_player(entity_data)
    if entity_type == "mine":
        entity =  mine_loader.load_mine(entity_data)
    if entity_type == "flag":
        entity =  flag_loader.load_flag(entity_data)
    if entity_type == "door":
        entity =  door_loader.load_door(entity_data)
    if entity_type == "lever":
        entity =  lever_loader.load_lever(entity_data)
    if entity_type == "enemy":
        entity =  enemy_loader.load_enemy(entity_data)
    if entity_type == "projectile":
        entity =  projectile_loader.load_projectile(entity_data)

    if "model" in entity_data:
        entity["model"] = model_loader.load_model(entity_data["model"])

    entity_functions.init(entity)

    return entity