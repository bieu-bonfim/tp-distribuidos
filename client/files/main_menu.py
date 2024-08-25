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
import create_lobby
import game_screen
import shop_screen

# Screen title and size
SCREEN_WIDTH = 924
SCREEN_HEIGHT = 868
SCREEN_TITLE = "Cryptids: The Conspiracy Main Menu"
BASE_MARGIN = 30

MIDDLE_X = SCREEN_WIDTH/2
MIDDLE_Y = SCREEN_HEIGHT/2

class MainMenu(arcade.View):
    """ Main application class. """

    def __init__(self, server, session):
        super().__init__()
        self.session = session
        self.game_server = server
        self.client = self.game_server.get_client(self.session)
        self.manager = arcade.gui.UIManager()
        self.manager.enable()
        self.go_to_edit = False
        self.data_dict = None
        self.go_to_shop = False
        self.player_coin = None
        self.monetario = 0


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

        self.background = arcade.load_texture("/home/sprites/main_menu.png")

        self.manager.add(
            arcade.gui.UIAnchorWidget(
                anchor_x="center_x",
                anchor_y="center_y",
                align_y=-200,
                child=self.v_box)
        )

    def on_click_play(self, event):
        create_lobby_window = create_lobby.CreateLobby(self.game_server, self.session)
        self.window.show_view(create_lobby_window)

    def on_click_edit(self, event):
        self.game_server.bap()
        self.data_dict = self.game_server.load_inventory(self.client)
        self.go_to_edit = True
        
    def on_click_shop(self, event):
        self.monetario = self.client.get_moeda()
        self.go_to_shop = True


    def on_hide_view(self):
        self.manager.disable()
        self.manager.clear()



    def on_show_view(self):
        print("Menu principal iniciado")

    def on_draw(self):
        """ Render the screen. """
        # Clear the screen
        self.clear()
        arcade.draw_lrwh_rectangle_textured(0, 0, 1412, 868, self.background)
        self.manager.draw()

        if self.go_to_edit == True:
            edit_window = edit_deck.EditDeck(client=self.client, data_chunk=self.data_dict, game_server=self.game_server)
            edit_window.setup()
            self.window.show_view(edit_window)

        if self.go_to_shop == True:
            shop_window = shop_screen.ShopScreen(self.game_server, self.client, self.monetario)
            shop_window.setup()
            self.window.show_view(shop_window)