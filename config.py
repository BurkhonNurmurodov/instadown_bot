from telebot import types
import json as js

def get_json(filename):
    with open(filename, 'r') as file:
        return js.load(file)

def get_text(profile:str):
    try:
        with open(f"{profile}/data.json", "rb") as data:
            return js.load(data)["node"]["edge_media_to_caption"]["edges"][0]["node"]["text"]
    except:
            return ""

def add_json(filename, data):
    with open(filename, 'w') as file:
        js.dump(data, file)

def is_user(id):
    users = get_json("users.json")
    res = False
    for user_id in users:
        if user_id ==id:
            res = True
            break
    return res