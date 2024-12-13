import data_provider
import loaders.entity_loader as entity_loader
import loaders.tilemap_loader as tilemap_loader

def load_level(name):

    data = data_provider.get_level_data(name)

    
    level_data = {}

    level_data["camera"] = {
        "x":0,
        "y":0,
        "margin":250
    }

    entities_data = data["entities"]

    level_entities = []
    for entity_data in entities_data:
        level_entities.append(entity_loader.load_entity(entity_data))

    #TODO put player entity in front

    level_data["entities"] = level_entities

    tilemap_data = data["tilemap"]
    level_data["tilemap_object"] = tilemap_loader.load_tilemap(tilemap_data)

    level_data["level_width"] = level_data["tilemap_object"]["tile_map_width"] * level_data["tilemap_object"]["tile_width"]
    level_data["level_height"] = level_data["tilemap_object"]["tile_map_height"] * level_data["tilemap_object"]["tile_height"]

    stage = {
        "name" : "level",
        "data" : level_data}           
        
    
    return stage