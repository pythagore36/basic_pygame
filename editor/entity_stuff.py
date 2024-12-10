entity_data={}

entity_by_name = {}

def init():
    global entity_data, entity_by_name
    entities = [{
        "id":0,
        "name":"player",
        "image":"player",
        "fields":[]
    },{
        "id":1,
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
        "id":2,
        "name":"flag",
        "image":"flag",
        "fields":[]
    },{
        "id":3,
        "name":"door",
        "image":"door",
        "fields":[{
            "key":"open_condition",
            "default":"false"
        }]
    },{
        "id":4,
        "name":"enemy",
        "image":"enemy",
        "fields":[]
    },{
        "id":5,
        "name":"lever",
        "image":"lever",
        "fields":[{
            "key":"state",
            "default":0
        },{
            "key":"id",
            "default":-1
        }]
    }
    ]
    entity_data["entities"] = entities
    entity_data["image_width"] = 40
    entity_data["image_height"] = 40

    for entity in entity_data["entities"]:
        entity_by_name[entity["name"]] = entity

def get_entity_data():
    return entity_data

def get_image_by_entity_name(name):
    return entity_by_name[name]["image"]

def get_fields_by_entity_name(name):
    return entity_by_name[name]["fields"]