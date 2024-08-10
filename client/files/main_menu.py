import arcade
import arcade.gui
from arcade import load_texture
from arcade.gui import UIManager
from arcade.gui.widgets import UITextArea, UIInputText, UITexturePane
import random
import socket
import threading
import time
import client
import json
import edit_deck

# Screen title and size
SCREEN_WIDTH = 924
SCREEN_HEIGHT = 868
SCREEN_TITLE = "Cryptids: The Conspiracy Main Menu"
BASE_MARGIN = 30

MIDDLE_X = SCREEN_WIDTH/2
MIDDLE_Y = SCREEN_HEIGHT/2

class MainMenu(arcade.View):
    """ Main application class. """

    def __init__(self):
        super().__init__()

        self.manager = arcade.gui.UIManager()
        self.manager.enable()


        # Create a vertical BoxGroup to align buttons
        self.v_box = arcade.gui.UIBoxLayout()

        # Again, method 1. Use a child class to handle events.
        play_button = arcade.gui.UIFlatButton(text="Jogar", width=200)
        self.v_box.add(play_button.with_space_around(bottom=20))
        play_button.on_click = self.on_click_play


        edit_button = arcade.gui.UIFlatButton(text="Editar Decks", width=200)
        self.v_box.add(edit_button.with_space_around(bottom=20))
        edit_button.on_click = self.on_click_edit

        shop_button = arcade.gui.UIFlatButton(text="Loja de Cartas", width=200)
        self.v_box.add(shop_button.with_space_around(bottom=20))
        shop_button.on_click = self.on_click_shop

        self.flag_deck = 0
        self.flag_game = 0
        self.flag_shop = 0


        arcade.set_background_color(arcade.color.CHARLESTON_GREEN)

        # Create a widget to hold the v_box widget, that will center the buttons
        self.manager.add(
            arcade.gui.UIAnchorWidget(
                anchor_x="center_x",
                anchor_y="center_y",
                child=self.v_box)
        )

    def on_click_play(self, event):
        print("play")

    def on_click_edit(self, event):
        print("edit")
        edit_window = edit_deck.EditDeck()
        edit_window.setup()
        self.window.show_view(edit_window)

    def on_click_shop(self, event):
        print("shop")

    def on_hide_view(self):
        self.manager.disable()
        self.manager.clear()



    def on_show_view(self):
        print("Menu principal iniciado")

        #thread_receive = threading.Thread(target=self.receive_message, args=(s,))
        #thread_receive.start()

        #data = {'header': 'player_connection','player_name_register': player_name}
        #data_str = json.dumps(data)

        #try:
        #    s.sendall(bytes(data_str,encoding="utf-8"))
        #except socket.error as e:
        #    print(str(e))

    def on_draw(self):
        """ Render the screen. """
        # Clear the screen
        self.clear()
        self.manager.draw()

        #arcade.draw_rectangle_filled(MIDDLE_X, (MIDDLE_Y+60), 140, 30, arcade.color.WHITE)
        #arcade.draw_rectangle_outline(MIDDLE_X, (MIDDLE_Y+60), 140, 30, arcade.color.BLACK)
        
        # Draw the text
        #arcade.draw_text(self.login, MIDDLE_X, MIDDLE_Y+60, arcade.color.BLACK, 14, anchor_x="left", anchor_y="center")



def start_menu():
    
    #port = int(input('Enter port: '))

    #s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #s.connect((host, port))


    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    start_view = MainMenu()
    window.show_view(start_view)
    start_view.setup()
    #arcade.run()
    #return s