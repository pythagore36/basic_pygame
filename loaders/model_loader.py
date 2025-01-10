import data_provider
import image_manager

models = {}


def load_model(key):
    global models
    if key in models:
        return models[key]
    model = data_provider.get_model_data(key)
    if model == None:
        return None    
    if "sprites" in model:
        for sprite in model["sprites"]:
            sprite_data = None
            if "model_sprites" in model and sprite in model["model_sprites"]:
                sprite_data = model["model_sprites"][sprite]
            else:
                sprite_data = data_provider.get_sprite_data(sprite)
            if sprite_data != None:
                image_manager.load_sprite(sprite_data)
    models[key] = model
    return model
    