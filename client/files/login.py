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
        arcade.draw_rectangle_filled(self.x, self.y, self.width, self.height, arcade.color.WHITE)
        arcade.draw_rectangle_outline(self.x, self.y, self.width, self.height, arcade.color.BLACK)
        
        # Draw the text
        arcade.draw_text(self.text, self.x - self.width//2 + 5, self.y, arcade.color.BLACK, 14, anchor_x="left", anchor_y="center")

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



class Login(arcade.View):
    """ Main application class. """

    def __init__(self):
        super().__init__()

        self.manager = arcade.gui.UIManager()
        self.manager.enable()
        self.loginText = TextBox((SCREEN_WIDTH//2), (SCREEN_HEIGHT//2)+80, 250, 40) 
        self.active = False


        # Create a vertical BoxGroup to align buttons
        self.v_box = arcade.gui.UIBoxLayout()

        login_button = arcade.gui.UIFlatButton(text="Login", width=200)
        self.v_box.add(login_button.with_space_around(bottom=20))
        login_button.on_click = self.on_click_login



        arcade.set_background_color(arcade.color.CHARLESTON_GREEN)

        # Create a widget to hold the v_box widget, that will center the buttons
        self.manager.add(
            arcade.gui.UIAnchorWidget(
                anchor_x="center_x",
                anchor_y="center_y",
                child=self.v_box)
        )


    def on_click_login(self, event):
        print(self.loginText.text)
        menu_main = main_menu.MainMenu()
        self.window.show_view(menu_main)

    def on_draw(self):
        """ Render the screen. """
        # Clear the screen
        self.clear()
        self.manager.draw()
        self.loginText.draw()

        #arcade.draw_rectangle_filled(MIDDLE_X, (MIDDLE_Y+60), 140, 30, arcade.color.WHITE)
        #arcade.draw_rectangle_outline(MIDDLE_X, (MIDDLE_Y+60), 140, 30, arcade.color.BLACK)
        
        # Draw the text
        #arcade.draw_text(self.login, MIDDLE_X, MIDDLE_Y+60, arcade.color.BLACK, 14, anchor_x="left", anchor_y="center")

    def on_key_press(self, symbol, modifiers):
            self.loginText.on_key_press(symbol, modifiers)

    def on_mouse_press(self, x, y, button, modifiers):
            self.loginText.on_mouse_press(x, y, button, modifiers)




