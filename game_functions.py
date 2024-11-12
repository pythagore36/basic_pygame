import renderer
import stages.stage_functions as stage_functions
import loaders.level_loader as level_loader


def init_game_data():
    game_data = {
    "running":True,
    "screen_width":608,
    "screen_height":608,
    "stage":{
        "name": "introduction",
        "data": {"timer":120}
    }
}

    return game_data

def set_stage(name, game_data):
    if name == "introduction":
        game_data["stage"] = {
        "name": "introduction",
        "data": {"timer":120}
        }
    elif name == "congratulations":
        game_data["stage"] = {
        "name": "congratulations",
        "data": {"timer":120}
        }
    elif name == "game_over":
        game_data["stage"] = {
        "name": "game_over",
        "data": {"timer":120}
        }
    elif name == "level":
        game_data["stage"] = level_loader.load_level("level1")


def apply_message(message, game_data):
    if message["type"] == "set_stage":
        set_stage(message["object"], game_data)
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