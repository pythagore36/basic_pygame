import renderer
import stages.stage_functions as stage_functions
import loaders.level_loader as level_loader
import data_provider


def init_game_data():
    game_data = {
    "running":True,
    "screen_width":data_provider.get_variable("screen_width"),
    "screen_height":data_provider.get_variable("screen_height"),
    "stage":{
        "name": "introduction",
        "data": {"timer":120}
    },
    "current_level":data_provider.get_variable("entry_level")
}

    return game_data

def set_stage(name, game_data):
    stage_functions.load(name,game_data)


def apply_message(message, game_data):
    if message["type"] == "set_stage":
        set_stage(message["object"], game_data)
    elif message["type"] == "change_current_level":
        game_data["current_level"] = message["object"]
    elif message["type"] == "change_next_level":
        game_data["next_level"] = message["object"]
    elif message["type"] == "terminate_game":
        game_data["running"] = False

def update(game_data):

    game_data["messages"] = []

    stage = game_data["stage"]
    stage_functions.update(stage, game_data)

    for message in game_data["messages"]:
        apply_message(message, game_data)
                

def render(game_data):
    stage = game_data["stage"]

    renderer.init_frame()
    
    stage_functions.render(stage, game_data)
    
    renderer.refresh_screen()