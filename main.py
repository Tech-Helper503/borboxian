from tkinter import font
from turtle import position
from ursina import *
from ursinanetworking import UrsinaNetworkingServer, UrsinaNetworkingClient

from utils.utils import calculate_font_offset
from scene import Scene
from world import World

window.borderless = False
window.title = 'Borboxian'
window.fullscreen = False

application.development_mode = False

app = Ursina()

default_font = 'assets/IBMPlexMono-Regular.ttf'
Text.default_font = default_font
default_font_offset = 0.375

# Set window color

window.color = color.color(1/51,1/51,1/51)

# Entity has to be instantiated into the Ursina scope

window.exit_button.visible = False
window.fps_counter.enabled = False

scenes = []
main_menu_scene = Scene(True)
example_game_scene = Scene(False)
multi_player_panel_scene = Scene(False)

scenes.append(main_menu_scene)
scenes.append(example_game_scene)
scenes.append(multi_player_panel_scene)



def main_menu():

    title = Text('Borboxian', position=(0,0.5),always_on_top=True)

    play_button = Button(position=(0,0.05), text='Singleplayer',scale=(0.3,0.075), color=color.red, radius=0)
    play_button.on_click = example_game

    
    multi_player = Button(position=(0,-0.2), text='Multiplayer', color=color.red, radius=0,scale=(0.3,0.075))
    multi_player.on_click = multi_player_panel

    main_menu_scene.entities.append(play_button)
    main_menu_scene.entities.append(multi_player)

    main_menu_scene.entities.append(title)


def example_game():
    if main_menu_scene.is_current_scene == True:
        main_menu_scene.transition(example_game_scene)
        world = World(False)
        example_game_scene.transition(world)
        world.world_gen()

def multi_player_panel():
    if main_menu_scene.is_current_scene == True:
        main_menu_scene.transition(multi_player_panel_scene)
        panel = Entity(model = 'quad', scale=(5,5))
        panel.color = color.gray
        panel.radius = 0

main_menu()


def update():
    for scene in scenes:
        if scene.is_current_scene == True:
            scene.update()

app.run()