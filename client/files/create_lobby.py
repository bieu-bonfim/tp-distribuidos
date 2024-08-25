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
import main_menu
import lobby_screen
import Pyro5.api
import os
import game_screen
from GameHandler import GameHandler

container_name = os.getenv("CONTAINER_NAME", "default_container_name")

# Screen title and size
SCREEN_WIDTH = 1412
SCREEN_HEIGHT = 868
SCREEN_TITLE = "Cryptids: The Conspiracy Login"
BASE_MARGIN = 30

MIDDLE_X = SCREEN_WIDTH/2
MIDDLE_Y = SCREEN_HEIGHT/2

host = 'server'
port = 8020
s = None


class TextBox:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = ""
        self.active = False

    def draw(self):
        # Draw the text box
        arcade.draw_rectangle_filled(self.x, self.y, self.width, self.height, arcade.color.EERIE_BLACK)
        arcade.draw_rectangle_outline(self.x, self.y, self.width, self.height, arcade.color.ENGLISH_VIOLET)
        
        # Draw the text
        arcade.draw_text(self.text, self.x - self.width//2 + 5, self.y, arcade.color.WHITE, 14, anchor_x="left", anchor_y="center")

    def on_key_press(self, symbol, modifiers):
        if self.active:
            if symbol == arcade.key.BACKSPACE:
                self.text = self.text[:-1]
            elif symbol == arcade.key.ENTER or symbol == arcade.key.RETURN:
                self.active = False
            else:
                self.text += chr(symbol)

    def on_mouse_press(self, x, y, button, modifiers):
        if (self.x - self.width // 2 < x < self.x + self.width // 2 and
            self.y - self.height // 2 < y < self.y + self.height // 2):
            self.active = True
        else:
            self.active = False


class CreateLobby(arcade.View):
    """ Main application class. """

    def __init__(self, game_server, session):
        super().__init__()
        self.session = session
        self.game_server = Pyro5.api.Proxy(game_server._pyroUri)
        self.client = self.game_server.get_client(self.session)
        self.manager = arcade.gui.UIManager()
        self.manager.enable()
        self.lobbyText = TextBox((SCREEN_WIDTH//2), (SCREEN_HEIGHT//2)-100, 250, 40) 
        self.active = False
        self.go_to_lobby = False
        self.lobby_data = None
        self.gameHandler = None

        # Create a vertical BoxGroup to align buttons
        self.v_box = arcade.gui.UIBoxLayout()

        enter_lobby_button = arcade.gui.UIFlatButton(text="Entrar em Sala", width=200)
        self.v_box.add(enter_lobby_button.with_space_around(bottom=20))
        enter_lobby_button.on_click = self.on_click_enter_lobby

        create_lobby_button = arcade.gui.UIFlatButton(text="Criar Sala", width=200)
        self.v_box.add(create_lobby_button.with_space_around(bottom=20))
        create_lobby_button.on_click = self.on_click_create_lobby

        voltar_button = arcade.gui.UIFlatButton(text="Voltar", width=200)
        self.v_box.add(voltar_button.with_space_around(bottom=20))
        voltar_button.on_click = self.on_click_voltar

        self.background = arcade.load_texture("/home/sprites/main_menu.png")

        # Create a widget to hold the v_box widget, that will center the buttons
        self.manager.add(
            arcade.gui.UIAnchorWidget(
                anchor_x="center_x",
                anchor_y="center_y",
                align_y=-250,
                child=self.v_box)
        )

    def on_click_voltar(self, event):
        menu = main_menu.MainMenu(self.game_server, self.session)
        self.window.show_view(menu)

    def on_click_create_lobby(self, event):
        self.lobby_data = self.game_server.create_lobby(self.client)
        self.gameHandler = GameHandler(
            lobby_screen.LobbyScreen(
                self.game_server, 
                self.session, 
                self.lobby_data['players'], 
                self.lobby_data['index'])
            )
        self.register_connection(self.game_server, self.session, self.lobby_data['index'])
        self.go_to_lobby = True

    def on_click_enter_lobby(self, event):
        self.lobby_data = self.game_server.join_lobby(int(self.lobbyText.text), self.client)
        self.gameHandler = GameHandler(
            lobby_screen.LobbyScreen(
                self.game_server, 
                self.session, 
                self.lobby_data['players'], 
                self.lobby_data['index'])
            )
        self.register_connection(self.game_server, self.session, self.lobby_data['index'])
        self.go_to_lobby = True

    def on_draw(self):
        """ Render the screen. """
        # Clear the screen
        self.clear()
        arcade.draw_lrwh_rectangle_textured(0, 0, 1412, 868, self.background)
        self.manager.draw()
        self.lobbyText.draw()

        if self.go_to_lobby == True:
            lobby = self.gameHandler.lobby_screen
            lobby.setup()
            self.window.show_view(lobby)


        #arcade.draw_rectangle_filled(MIDDLE_X, (MIDDLE_Y+60), 140, 30, arcade.color.WHITE)
        #arcade.draw_rectangle_outline(MIDDLE_X, (MIDDLE_Y+60), 140, 30, arcade.color.BLACK)
        
        # Draw the text
        #arcade.draw_text(self.login, MIDDLE_X, MIDDLE_Y+60, arcade.color.BLACK, 14, anchor_x="left", anchor_y="center")

    def on_key_press(self, symbol, modifiers):
            self.lobbyText.on_key_press(symbol, modifiers)

    def on_mouse_press(self, x, y, button, modifiers):
            self.lobbyText.on_mouse_press(x, y, button, modifiers)

    def register_connection(self, server, session, index):
        server = Pyro5.api.Proxy(server._pyroUri)
        client = server.get_client(session)
        daemon = Pyro5.api.Daemon(host=container_name)
        client_uri = daemon.register(self.gameHandler)
        server.register(client, client_uri, index)
        print(f"Client {client.get_username()} registered with URI: {client_uri}")
        threading.Thread(target=daemon.requestLoop, daemon=True).start()





