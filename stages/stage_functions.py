import stages.introduction as introduction
import stages.level as level
import stages.congratulations as congratulations
import stages.game_over as game_over
import stages.level_transition as level_transition
import loaders.level_loader as level_loader
import stages.level_finished as level_finished

def load(name, game_data):
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
        game_data["stage"] = level_loader.load_level(game_data["current_level"])
    elif name == "level_transition":
        game_data["stage"] = {
        "name": "level_transition",
        "data": {"timer":120}
        }
    elif name == "level_finished":
        game_data["stage"] = {
        "name": "level_finished",
        "data": {"timer":120}
        }

def update(stage, game_data):
    if stage["name"] == "introduction":
        introduction.update(stage["data"], game_data)
    elif stage["name"] == "level":
        level.update(stage["data"], game_data)
    elif stage["name"] =="congratulations":
        congratulations.update(stage["data"], game_data)
    elif stage["name"] =="game_over":
        game_over.update(stage["data"], game_data)
    elif stage["name"] =="level_transition":
        level_transition.update(stage["data"], game_data)
    elif stage["name"] =="level_finished":
        level_finished.update(stage["data"], game_data)

def render(stage, game_data):
    if stage["name"] == "introduction":
        introduction.render(stage["data"], game_data)
    elif stage["name"] == "level":
        level.render(stage["data"], game_data)
    elif stage["name"] =="congratulations":
        congratulations.render(stage["data"], game_data)
    elif stage["name"] =="game_over":
        game_over.render(stage["data"], game_data)
    elif stage["name"] =="level_transition":
        level_transition.render(stage["data"], game_data)
    elif stage["name"] =="level_finished":
        level_finished.render(stage["data"], game_data)