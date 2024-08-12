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

sem = threading.Semaphore()

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

    def __init__(self, client):
        super().__init__()
        self.client = client
        self.manager = arcade.gui.UIManager()
        self.manager.enable()
        self.lobbyText = TextBox((SCREEN_WIDTH//2), (SCREEN_HEIGHT//2)-100, 250, 40) 
        self.active = False

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

        threading.Thread(target=self.receive_message).start()



    def on_click_voltar(self, event):
        menu = main_menu.MainMenu(self.client)
        self.window.show_view(menu)

    def on_click_create_lobby(self, event):
        data = {'header': 'create_lobby', 'request': {}}
        time.sleep(1)
        self.client.sendMessage(data)
        print("create lobby")


    def on_click_enter_lobby(self, event):
        data = {'header': 'join_lobby', 'request': {'index': self.lobbyText.text}}
        time.sleep(1)
        self.client.sendMessage(data)
        print(self.lobbyText.text)

    def on_draw(self):
        """ Render the screen. """
        # Clear the screen
        self.clear()
        arcade.draw_lrwh_rectangle_textured(0, 0, 1412, 868, self.background)
        self.manager.draw()
        self.lobbyText.draw()


        #arcade.draw_rectangle_filled(MIDDLE_X, (MIDDLE_Y+60), 140, 30, arcade.color.WHITE)
        #arcade.draw_rectangle_outline(MIDDLE_X, (MIDDLE_Y+60), 140, 30, arcade.color.BLACK)
        
        # Draw the text
        #arcade.draw_text(self.login, MIDDLE_X, MIDDLE_Y+60, arcade.color.BLACK, 14, anchor_x="left", anchor_y="center")

    def on_key_press(self, symbol, modifiers):
            self.lobbyText.on_key_press(symbol, modifiers)

    def on_mouse_press(self, x, y, button, modifiers):
            self.lobbyText.on_mouse_press(x, y, button, modifiers)

    def receive_message(self):
            try:
                data_dict = self.client.receiveMessage()
                print("DATA DATA - ", data_dict)

                if data_dict['header'] == 'lobby_created':
                    if data_dict['response']['status'] == "success":
                        menu = lobby_screen.LobbyScreen(self.client, [])
                        menu.setup()
                        self.window.show_view(menu)
                    
                elif data_dict['header'] == 'join_lobby':
                    if data_dict['response']['status'] == "success":     
                        array_players = data_dict['response']['data']['lobby']['players']     
                        print(array_players)
                        menu = lobby_screen.LobbyScreen(self.client, array_players)
                        menu.setup()
                        self.window.show_view(menu)

            except socket.error as e:
                print(str(e))




