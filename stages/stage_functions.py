import stages.introduction as introduction
import stages.level as level
import stages.congratulations as congratulations
import stages.game_over as game_over

def update(stage, game_data):
    if stage["name"] == "introduction":
        introduction.update(stage["data"], game_data)
    elif stage["name"] == "level":
        level.update(stage["data"], game_data)
    elif stage["name"] =="congratulations":
        congratulations.update(stage["data"], game_data)
    elif stage["name"] =="game_over":
        game_over.update(stage["data"], game_data)

def render(stage, game_data):
    if stage["name"] == "introduction":
        introduction.render(stage["data"], game_data)
    elif stage["name"] == "level":
        level.render(stage["data"], game_data)
    elif stage["name"] =="congratulations":
        congratulations.render(stage["data"], game_data)
    elif stage["name"] =="game_over":
        game_over.render(stage["data"], game_data)