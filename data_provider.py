import json

data_path = "data/data_directory.txt"

data_directory = {}
levels = {}
models = {}
sprites = {}

def init():
    global data_directory, levels, models, sprites
    f = open(data_path, "r")
    data_directory = json.load(f)

    if "levels" in data_directory:
        for level in data_directory["levels"]:
            levels[level["key"]] = level
    if "models" in data_directory:
        for model in data_directory["models"]:
            models[model["key"]] = model
    if "sprites" in data_directory:
        for sprite in data_directory["sprites"]:
            sprites[sprite["key"]] = sprite

def append_sprite_data(model_sprites):
    global sprites
    for sprite in model_sprites:
        sprites[sprite["key"]] = sprite

def get_level_data(key):
    if key in levels:
        level = levels[key]
        f = open(level["path"], "r")
        data = json.load(f)
        return data
    return None

def get_model_data(key):
    if key in models:
        model = models[key]
        f = open(model["path"], "r")
        data = json.load(f)
        return data
    return None

def get_sprite_data(key):
    if key in sprites:
        return sprites[key]
    return None

def get_variable(name):
    if name in data_directory:
        return data_directory[name]
    return None

def get_level_name(key):
    if key in levels:
        level = levels[key]
        return level["name"]
    return None