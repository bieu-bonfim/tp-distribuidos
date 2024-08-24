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
import Pyro5.api

# Screen title and size
SCREEN_WIDTH = 1412
SCREEN_HEIGHT = 868
SCREEN_TITLE = "Cryptids: The Conspiracy Login"
BASE_MARGIN = 30

MIDDLE_X = SCREEN_WIDTH/2
MIDDLE_Y = SCREEN_HEIGHT/2
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


class KeyBox:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = ""
        self.symbol = ""
        self.active = False

    def draw(self):
        # Draw the text box
        arcade.draw_rectangle_filled(self.x, self.y, self.width, self.height, arcade.color.EERIE_BLACK)
        arcade.draw_rectangle_outline(self.x, self.y, self.width, self.height, arcade.color.ENGLISH_VIOLET)
        
        # Draw the text
        arcade.draw_text(self.symbol, self.x - self.width//2 + 5, self.y, arcade.color.WHITE, 14, anchor_x="left", anchor_y="center")

    def on_key_press(self, symbol, modifiers):
        if self.active:
            if symbol == arcade.key.BACKSPACE:
                self.text = self.text[:-1]
                self.symbol = self.symbol[:-1]
            elif symbol == arcade.key.ENTER or symbol == arcade.key.RETURN:
                self.active = False
            else:
                self.text += chr(symbol)
                self.symbol += "*"

    def on_mouse_press(self, x, y, button, modifiers):
        if (self.x - self.width // 2 < x < self.x + self.width // 2 and
            self.y - self.height // 2 < y < self.y + self.height // 2):
            self.active = True
        else:
            self.active = False



class Login(arcade.View):
    """ Main application class. """

    def __init__(self):
        super().__init__()
        self.manager = arcade.gui.UIManager()
        self.manager.enable()
        self.loginText = TextBox((SCREEN_WIDTH//2), (SCREEN_HEIGHT//2)-120, 250, 40) 
        self.loginKey = KeyBox((SCREEN_WIDTH//2), (SCREEN_HEIGHT//2)-200, 250, 40) 
        self.active = False
        self.key_active = False
        self.valid_login = False


        # Create a vertical BoxGroup to align buttons
        self.v_box = arcade.gui.UIBoxLayout()

        login_button = arcade.gui.UIFlatButton(text="Login", width=200)
        self.v_box.add(login_button.with_space_around(bottom=20))
        login_button.on_click = self.on_click_login



        self.background = arcade.load_texture("/home/sprites/main_menu.png")

        # Create a widget to hold the v_box widget, that will center the buttons
        self.manager.add(
            arcade.gui.UIAnchorWidget(
                anchor_x="center_x",
                anchor_y="center_y",
                align_y=-300,
                child=self.v_box)
        )


    def on_click_login(self, event):
        print(self.loginText.text)
        print(self.loginKey.text)
        ns = Pyro5.api.locate_ns(host='pyro-ns', port=8020)
        print("bap 1")
        uri = ns.lookup("cryptids.server")
        print("bap 2")
        server = Pyro5.api.Proxy(uri)
        print("bap 3")
        if server.connect_client(self.loginText.text, self.loginKey.text):
            self.valid_login = True

    def on_draw(self):
        """ Render the screen. """
        # Clear the screen
        self.clear()
        arcade.draw_lrwh_rectangle_textured(0, 0, 1412, 868, self.background)
        self.manager.draw()
        self.loginText.draw()
        self.loginKey.draw()

        if self.valid_login:
            menu_main = main_menu.MainMenu(self.client)
            self.window.show_view(menu_main)


        #arcade.draw_rectangle_filled(MIDDLE_X, (MIDDLE_Y+60), 140, 30, arcade.color.WHITE)
        #arcade.draw_rectangle_outline(MIDDLE_X, (MIDDLE_Y+60), 140, 30, arcade.color.BLACK)
        
        # Draw the text
        #arcade.draw_text(self.login, MIDDLE_X, MIDDLE_Y+60, arcade.color.BLACK, 14, anchor_x="left", anchor_y="center")

    def on_key_press(self, symbol, modifiers):
            self.loginText.on_key_press(symbol, modifiers)
            self.loginKey.on_key_press(symbol, modifiers)

    def on_mouse_press(self, x, y, button, modifiers):
            self.loginText.on_mouse_press(x, y, button, modifiers)
            self.loginKey.on_mouse_press(x, y, button, modifiers)

    def receive_message(self, client_socket):
        while True:
            try:
                data = client_socket.recv(1024)
                #print(f"DATA DATA - {data.decode()}")
                data_dict = json.loads(data.decode("utf-8"))


                
                if data_dict['header'] == 'login':
                    if data_dict['response']['data'] != {}:
                        data = data_dict['response']['data']
                        self.client.client_id = data['user_id']
                        self.client.client_name = data['username']
                        self.client.client_email = data['email']
                        self.valid_login = True
                        data = {'header': 'ACK', 'request': {}}
                        self.client.sendMessage(data)
                        break
                        

            except socket.error as e:
                print(str(e))
                break




