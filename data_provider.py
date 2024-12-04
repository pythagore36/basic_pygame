import json

def get_data(name):
    f = open("level_data_edited.txt", "r")
    data = json.load(f)
    return data