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
import create_lobby
import game_screen

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


class LobbyScreen(arcade.View):
    """ Main application class. """

    def __init__(self, client, players_on_lobby):
        super().__init__()
        self.client = client
        self.manager = arcade.gui.UIManager()
        self.data_dict = None
        self.manager.enable()
        self.active = False
        self.players_on_lobby = players_on_lobby
        self.opponent1 = "Aguardando..."
        self.opponent2 = "Aguardando..."
        self.back_to_creation = False
        self.start_game = False
        self.own_deck = None
        self.deck_loaded = False
        self.array_players = None

        # Create a vertical BoxGroup to align buttons
        self.v_box = arcade.gui.UIBoxLayout()

        ready_button = arcade.gui.UIFlatButton(text="Iniciar Jogo", width=200)
        self.v_box.add(ready_button.with_space_around(bottom=20))
        ready_button.on_click = self.on_click_ready_button

        voltar_button = arcade.gui.UIFlatButton(text="Voltar", width=200)
        self.v_box.add(voltar_button.with_space_around(bottom=20))
        voltar_button.on_click = self.on_click_voltar

        self.background = arcade.load_texture("/home/sprites/lobby_screen.png")

        # Create a widget to hold the v_box widget, that will center the buttons
        self.manager.add(
            arcade.gui.UIAnchorWidget(
                anchor_x="center_x",
                anchor_y="center_y",
                align_y=-250,
                child=self.v_box)
        )


    def on_click_ready_button(self, event):
        data = {'header': 'start_game', 'request': {}}      
        self.client.sendMessage(data)

    def on_click_voltar(self, event):
        data = {'header': 'leave_lobby', 'request': {}} 
        self.client.sendMessage(data)

    def setup(self):
        for player in self.players_on_lobby:
             if player == self.client.client_name:
                continue
             elif self.opponent1 == "Aguardando...":
                self.opponent1 = player
             elif self.opponent2 == "Aguardando...":
                self.opponent2 = player
        threading.Thread(target=self.receive_message).start()
        print(self.opponent1)
        print(self.opponent2)

    def on_draw(self):
        """ Render the screen. """
        # Clear the screen
        self.clear()
        arcade.draw_lrwh_rectangle_textured(0, 0, 1412, 868, self.background)
        self.manager.draw()

        if self.start_game:
            #data = { 'header': 'retrieve_deck', 'request': {} }
            #self.client.sendMessage(data)
            #if self.deck_loaded:
            print("---------- GAME STARTED ----------")
            game = game_screen.Game(self.client, self.opponent1, self.opponent2, self.array_players)
            game.setup()
            self.window.show_view(game)

        if self.back_to_creation:
            create_lobby_window = create_lobby.CreateLobby(self.client)
            self.window.show_view(create_lobby_window)

        rect_width = 280
        rect_height = 40
        margin = 5
        text_color = arcade.color.WHITE
        rectangles = [
            (f"Oponente 1: {self.opponent1}", MIDDLE_X - rect_width - margin - (rect_width + margin) / 2, MIDDLE_Y - 100),
            (f"{self.client.client_name}", MIDDLE_X, MIDDLE_Y - 100),
            (f"Oponente 2: {self.opponent2}", MIDDLE_X + rect_width + margin + (rect_width + margin) / 2, MIDDLE_Y - 100)
        ]

        for text, x, y in rectangles:
            arcade.draw_rectangle_filled(x, y, rect_width, rect_height, arcade.color.EERIE_BLACK)
            arcade.draw_rectangle_outline(x, y, rect_width, rect_height, arcade.color.ENGLISH_VIOLET)
            arcade.draw_text(text, x, y, text_color, font_size=14, anchor_x="center", anchor_y="center")


    def receive_message(self):
        print('waiting for message')
        while True:
            try:
                self.data_dict = self.client.receiveMessage()
                print(f"Lobby screen got the message: {self.data_dict}")

                if self.data_dict['header'] == 'join_lobby' or self.data_dict['header'] == 'player_leave_lobby':
                    print(f"Joining lobby")
                    if self.data_dict['response']['status'] == "success":     
                        self.opponent1 = "Aguardando..."
                        self.opponent2 = "Aguardando..."
                        self.array_players = self.data_dict['response']['data']['lobby']['players']     
                        for player in self.array_players:
                            print(f"jogador entrou {player}")
                            if player == self.client.client_name:
                                continue
                            elif self.opponent1 == "Aguardando...":
                                self.opponent1 = player
                            elif self.opponent2 == "Aguardando...":
                                self.opponent2 = player
                    data = {'header': 'ACK', 'request': {}}
                    self.client.sendMessage(data)
                elif self.data_dict['header'] == 'leave_lobby':
                    print(f"Leaving lobby")
                    self.back_to_creation = True
                    data = {'header': 'ACK', 'request': {}}
                    self.client.sendMessage(data)
                    break
                elif self.data_dict['header'] == 'start_game':
                    print('vish...')
                    data = {'header': 'ACK', 'request': {}}
                    self.client.sendMessage(data)
                    self.start_game = True
                    break
                elif self.data_dict['header'] == 'retrieve_deck':
                    self.own_deck = self.data_dict['response']['data']['deck']['cards']
                    data = {'header': 'ACK', 'request': {}}
                    self.client.sendMessage(data)
                    self.deck_loaded = True
                    break

            except Exception as e:
                print(str(e))
                




