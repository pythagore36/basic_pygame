import entities.player_functions as player_functions
import entities.enemy_functions as enemy_functions

def apply_message(message):
    receiving_entity = message["to"]
    if receiving_entity["type"] == "player":
        player_functions.apply_message(message)
    elif receiving_entity["type"] == "enemy":
        enemy_functions.apply_message(message)