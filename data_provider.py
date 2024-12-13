import json

data_path = "data/data_directory.txt"

data_directory = {}

def init():
    global data_directory
    f = open(data_path, "r")
    data_directory = json.load(f)
    

def get_level_data(key):
    level = None
    if "levels" in data_directory:
        for l in data_directory["levels"]:
            if key == l["key"]:
                level = l

    if level != None:
        f = open(level["file"], "r")
        data = json.load(f)
        return data

def get_variable(name):
    if name in data_directory:
        return data_directory[name]
    return None

def get_level_name(key):
    level = None
    if "levels" in data_directory:
        for l in data_directory["levels"]:
            if key == l["key"]:
                level = l
    if level != None:
        return level["name"]
    return None