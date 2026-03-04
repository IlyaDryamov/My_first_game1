# 🟩🌲💭🛩️🌀🔥♥️🌊🪣🏆 🏩 🏰 ⬛🚁

import pynput
from map import Map
import time
import json
import os
from airplane import Airplane as Airp
from pynput import keyboard
from clouds import Clouds

TICK_SLEEP = 0.05
TREE_UPDATE = 50
CLOUDS_UPDATE = 100
FIRE_UPDATE = 75
MAP_W, MAP_H = 20, 10

field = Map(MAP_W, MAP_H)
clouds = Clouds(MAP_W, MAP_H)
airp = Airp(MAP_W, MAP_H)
tick = 1

MOVES = {"w": (-1, 0), 'd': (0, 1), 's': (1, 0), 'a': (0, -1)}
# f - сохранение, g - восстановление
def process_key(key):
    global airp, tick, clouds, field
    c = key.char.lower()
    # обработка движения игры
    if c in MOVES.keys():
        dx, dy = MOVES[c][0], MOVES[c][1]
        airp.move(dx, dy)
    # сохранение игры
    elif c == 'f':
        data = {"airplane": airp.export_data(), 
                "clouds": clouds.export_data(), 
                "field": field.export_data(),
                "tick": tick}
        
        with open("level.json", "w") as lvl:
            json.dump(data, lvl)
    # загрузка игры
    elif c == "g":
        with open("level.json", "r") as lvl:
            data = json.load(lvl)
            airp.import_data(data['airplane'])
            #field.import_data(data["field"])
            clouds.import_data(data["clouds"])

listener = keyboard.Listener(
    on_press=None,
    on_release=process_key)
listener.start()
while True:
    os.system ("cls") #cls для виндоус    clear для линукс
    field.process_airplane(airp, clouds)
    airp.print_stats()
    field.print_map(airp, clouds)
    print("TICK", tick)
    tick += 1
    time.sleep (TICK_SLEEP)
    if (tick % TREE_UPDATE == 0):
        field.generate_tree()
    if (tick % FIRE_UPDATE == 0):
        field.update_fires()
    if (tick % CLOUDS_UPDATE == 0):
        clouds.update()    


