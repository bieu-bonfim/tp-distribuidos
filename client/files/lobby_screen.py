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
import Pyro5.api

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

    def __init__(self, game_server, session, players_on_lobby, lobby_index):
        super().__init__()
        self.session = session
        self.lobby_index = lobby_index
        self.game_server = Pyro5.api.Proxy(game_server._pyroUri)
        self.client = self.game_server.get_client(self.session)
        self.player_name = self.client.get_username()
        self.manager = arcade.gui.UIManager()
        self.data_dict = None
        self.manager.enable()
        self.active = False
        self.players_on_lobby = players_on_lobby
        self.opponent1 = "Aguardando..."
        self.opponent2 = "Aguardando..."
        self.back_to_creation = False
        self.own_deck = None
        self.deck_loaded = False
        self.array_players = None
        self.go_to_game = False
        self.new_game_screen = None

        self.v_box = arcade.gui.UIBoxLayout()

        ready_button = arcade.gui.UIFlatButton(text="Iniciar Jogo", width=200)
        self.v_box.add(ready_button.with_space_around(bottom=20))
        ready_button.on_click = self.on_click_ready_button

        voltar_button = arcade.gui.UIFlatButton(text="Voltar", width=200)
        self.v_box.add(voltar_button.with_space_around(bottom=20))
        voltar_button.on_click = self.on_click_voltar

        self.background = arcade.load_texture("/home/sprites/lobby_screen.png")
        self.manager.add(
            arcade.gui.UIAnchorWidget(
                anchor_x="center_x",
                anchor_y="center_y",
                align_y=-250,
                child=self.v_box)
        )

    def bap(self):
        print("bap")

    def on_click_ready_button(self, event):
        self.game_server.trigger_lobby_start(self.lobby_index)
        # essa função deve alterar o atributo screen do GameHanlder
        # para isso, é necessário passar a tela como argumento na chamada
        # da função do game_server, algo do tipo:
        # self.trigger_lobby_game_start(self.lobby_index, ... ..., game_screen)
        # isso, claro, após inicializar a game_screen
        # em caso de dúvidas, consultar o arquivo create_lobby.py

    def on_click_voltar(self, event):
        self.game_server.leave_lobby(self.client)
        new_proxy = Pyro5.api.Proxy(self.game_server._pyroUri)
        if len(self.players_on_lobby) > 1:
            self.players_on_lobby.remove(self.player_name)
        new_proxy.trigger_lobby_update(self.lobby_index, self.players_on_lobby)
        # triggar outro lobby update com a nova lista de jogadores
        # a função leave_lobby retorna a lista de jogadores atualizada
        #---------------------------------------------------------------
        # além disso, a lógica da função deve ser alterada para remover o 
        # jogador da lista de jogadores, seu deck, e seu proxy
        self.back_to_creation = True

    def setup(self):
        new_proxy = Pyro5.api.Proxy(self.game_server._pyroUri)
        try:
            new_proxy.trigger_lobby_update(self.lobby_index, self.players_on_lobby)
        except Pyro5.errors.CommunicationError as e:
            print(f"Error communicating with server: {e}")
        except Pyro5.errors.PyroError as e:
            print(f"Pyro Error: {e}")
        
    def update_players(self, players):
        self.players_on_lobby = players
        self.opponent1 = "Aguardando..."
        self.opponent2 = "Aguardando..."
        for player in self.players_on_lobby:
            if player == self.player_name:
                continue
            elif self.opponent1 == "Aguardando...":
                self.opponent1 = player
            elif self.opponent2 == "Aguardando...":
                self.opponent2 = player
                
    def start_game(self, players):
        self.array_players = players
        self.go_to_game = True
        
    def on_draw(self):
        """ Render the screen. """
        # Clear the screen
        if self.go_to_game:
            self.new_game_screen = game_screen.Game(self.session, self.opponent1, self.opponent2, self.array_players, self.game_server, self.lobby_index)
            self.new_game_screen.setup()
            self.window.show_view(self.new_game_screen)
        
        self.clear()
        arcade.draw_lrwh_rectangle_textured(0, 0, 1412, 868, self.background)
        self.manager.draw()

        if self.back_to_creation:
            create_lobby_window = create_lobby.CreateLobby(self.game_server, self.session)
            self.window.show_view(create_lobby_window)

        rect_width = 280
        rect_height = 40
        margin = 5
        text_color = arcade.color.WHITE
        rectangles = [
            (f"Oponente 1: {self.opponent1}", MIDDLE_X - rect_width - margin - (rect_width + margin) / 2, MIDDLE_Y - 100),
            (f"{self.player_name}", MIDDLE_X, MIDDLE_Y - 100),
            (f"Oponente 2: {self.opponent2}", MIDDLE_X + rect_width + margin + (rect_width + margin) / 2, MIDDLE_Y - 100)
        ]

        for text, x, y in rectangles:
            arcade.draw_rectangle_filled(x, y, rect_width, rect_height, arcade.color.EERIE_BLACK)
            arcade.draw_rectangle_outline(x, y, rect_width, rect_height, arcade.color.ENGLISH_VIOLET)
            arcade.draw_text(text, x, y, text_color, font_size=14, anchor_x="center", anchor_y="center")


    # def receive_message(self):
    #     print('waiting for message')
    #     while True:
    #         try:
    #             self.data_dict = self.client.receiveMessage()
    #             print(f"Lobby screen got the message: {self.data_dict}")

    #             if self.data_dict['header'] == 'join_lobby' or self.data_dict['header'] == 'player_leave_lobby':
    #                 print(f"Joining lobby")
    #                 if self.data_dict['response']['status'] == "success":     
    #                     self.opponent1 = "Aguardando..."
    #                     self.opponent2 = "Aguardando..."
    #                     self.array_players = self.data_dict['response']['data']['lobby']['players']     
    #                     for player in self.array_players:
    #                         print(f"jogador entrou {player}")
    #                         if player == self.client.client_name:
    #                             continue
    #                         elif self.opponent1 == "Aguardando...":
    #                             self.opponent1 = player
    #                         elif self.opponent2 == "Aguardando...":
    #                             self.opponent2 = player
    #                 data = {'header': 'ACK', 'request': {}}
    #                 self.client.sendMessage(data)
    #             elif self.data_dict['header'] == 'leave_lobby':
    #                 print(f"Leaving lobby")
    #                 self.back_to_creation = True
    #                 data = {'header': 'ACK', 'request': {}}
    #                 self.client.sendMessage(data)
    #                 break
    #             elif self.data_dict['header'] == 'start_game':
    #                 print('vish...')
    #                 data = {'header': 'ACK', 'request': {}}
    #                 self.client.sendMessage(data)
    #                 self.start_game = True
    #                 break
    #             elif self.data_dict['header'] == 'retrieve_deck':
    #                 self.own_deck = self.data_dict['response']['data']['deck']['cards']
    #                 data = {'header': 'ACK', 'request': {}}
    #                 self.client.sendMessage(data)
    #                 self.deck_loaded = True
    #                 break

    #         except Exception as e:
    #             print(str(e))
                




