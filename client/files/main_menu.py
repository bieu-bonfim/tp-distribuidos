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

    def __init__(self, server, client):
        super().__init__()
        self.client = client
        self.manager = arcade.gui.UIManager()
        self.manager.enable()
        self.go_to_edit = False
        self.data_dict = None
        self.go_to_shop = False
        self.player_coin = None
        self.game_server = server


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

        # Create a widget to hold the v_box widget, that will center the buttons
        self.manager.add(
            arcade.gui.UIAnchorWidget(
                anchor_x="center_x",
                anchor_y="center_y",
                align_y=-200,
                child=self.v_box)
        )

    def on_click_play(self, event):
        create_lobby_window = create_lobby.CreateLobby(self.client)
        self.window.show_view(create_lobby_window)

    def on_click_edit(self, event):
        data = {'header': 'manage_inventory', 'request': {'user_id': self.client.client_id}}
        self.client.sendMessage(data)
        threading.Thread(target=self.receive_message).start()   
        
    def on_click_shop(self, event):
        data = {'header': 'get_moedas', 'request': {'user_id': self.client.client_id}}
        self.client.sendMessage(data)
        threading.Thread(target=self.receive_message).start()   

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
        arcade.draw_lrwh_rectangle_textured(0, 0, 1412, 868, self.background)
        self.manager.draw()

        #arcade.draw_rectangle_filled(MIDDLE_X, (MIDDLE_Y+60), 140, 30, arcade.color.WHITE)
        #arcade.draw_rectangle_outline(MIDDLE_X, (MIDDLE_Y+60), 140, 30, arcade.color.BLACK)
        
        # Draw the text
        #arcade.draw_text(self.login, MIDDLE_X, MIDDLE_Y+60, arcade.color.BLACK, 14, anchor_x="left", anchor_y="center")

        if self.go_to_edit == True:
            edit_window = edit_deck.EditDeck(self.client, self.data_dict['response']['data'])
            edit_window.setup()
            self.window.show_view(edit_window)

        if self.go_to_shop == True:
            shop_window = shop_screen.ShopScreen(self.client, self.player_coin)
            shop_window.setup()
            self.window.show_view(shop_window)
         

    def receive_message(self):
        while True:
            try:
                self.data_dict = self.client.receiveMessage()
                print(self.data_dict)
                
                if self.data_dict['header'] == 'show_user_inventory':
                    data = {'header': 'ACK', 'request': {}}
                    self.client.sendMessage(data)
                    self.go_to_edit = True            
                    break
                if self.data_dict['header'] == 'get_moedas':
                    self.player_coin = self.data_dict['response']['moedas']
                    data = {'header': 'ACK', 'request': {}}
                    self.client.sendMessage(data)
                    self.go_to_shop = True
                    break
            except Exception as e:
                print(str(e))