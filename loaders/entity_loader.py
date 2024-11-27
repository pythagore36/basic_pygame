import loaders.player_loader as player_loader
import loaders.mine_loader as mine_loader
import loaders.flag_loader as flag_loader
import loaders.door_loader as door_loader

def load_entity(entity_data):
    entity_type = entity_data["type"]
    if entity_type == "player":
        return player_loader.load_player(entity_data)
    if entity_type == "mine":
        return mine_loader.load_mine(entity_data)
    if entity_type == "flag":
        return flag_loader.load_flag(entity_data)
    if entity_type == "door":
        return door_loader.load_door(entity_data)