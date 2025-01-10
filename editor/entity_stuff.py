entity_data={}

entity_by_name = {}

def init():
    global entity_data, entity_by_name
    entities = [{
        "id":0,
        "name":"mine",
        "image":"mine",
        "fields":[{
            "key":"state",
            "default":"standing"
        },{
            "key":"patrolling_speed",
            "default":2
        },{
            "key":"patrolling_points",
            "default":"(0,0)"
        }]
    },{
        "id":1,
        "name":"flag",
        "image":"flag",
        "fields":[{
            "key":"model",
            "default":"blue_flag_model"
        },{
            "key":"destination",
            "default":""
        }]
    },{
        "id":2,
        "name":"door",
        "image":"door",
        "fields":[{
            "key":"model",
            "default":"door_model_1"
        },{
            "key":"open_condition",
            "default":"false"
        }]
    },{
        "id":3,
        "name":"enemy",
        "image":"enemy",
        "fields":[]
    },{
        "id":4,
        "name":"lever",
        "image":"lever",
        "fields":[{
            "key":"model",
            "default":"basic_lever_model"
        },{
            "key":"state",
            "default":0
        },{
            "key":"id",
            "default":-1
        }]
    }
    ]
    select_only_entities = [{
        "name":"player",
        "image":"player",
        "fields":[]
    }]
    entity_data["entities"] = entities
    entity_data["select_only_entities"] = select_only_entities
    entity_data["image_width"] = 40
    entity_data["image_height"] = 40

    for entity in entity_data["entities"]:
        entity_by_name[entity["name"]] = entity
    for entity in entity_data["select_only_entities"]:
        entity_by_name[entity["name"]] = entity


def get_entity_data():
    return entity_data

def get_image_by_entity_name(name):
    return entity_by_name[name]["image"]

def get_fields_by_entity_name(name):
    return entity_by_name[name]["fields"]

def can_remove_by_name(name):
    return entity_by_name[name] in entity_data["entities"]