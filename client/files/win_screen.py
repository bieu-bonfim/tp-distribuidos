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


class WInScreen(arcade.View):
    """ Main application class. """

    def __init__(self, client, winner):
        super().__init__()
        self.client = client
        self.manager = arcade.gui.UIManager()
        self.manager.enable()
        self.active = False
        self.key_active = False
        self.valid_login = False
        self.winner = winner


        # Create a vertical BoxGroup to align buttons
        self.v_box = arcade.gui.UIBoxLayout()

        voltar_menu = arcade.gui.UIFlatButton(text="Login", width=200)
        self.v_box.add(voltar_menu.with_space_around(bottom=20))
        voltar_menu.on_click = self.on_click_voltar



        self.background = arcade.load_texture("/home/sprites/end_screen.png")

        # Create a widget to hold the v_box widget, that will center the buttons
        self.manager.add(
            arcade.gui.UIAnchorWidget(
                anchor_x="center_x",
                anchor_y="center_y",
                align_y=-300,
                child=self.v_box)
        )


    def on_click_voltar(self, event):
        menu = main_menu.MainMenu(self.client)
        self.window.show_view(menu)

    def on_draw(self):
        """ Render the screen. """
        arcade.draw_rectangle_filled(MIDDLE_X, MIDDLE_Y - 100, 300, 150, arcade.color.EERIE_BLACK)
        arcade.draw_rectangle_outline(MIDDLE_X, MIDDLE_Y - 100, 300, 150, arcade.color.ENGLISH_VIOLET)
        arcade.draw_text(
            self.p1.name,
            start_x= MIDDLE_X,
            start_y= MIDDLE_Y - 100,
            color=arcade.color.WHITE,
            font_size=30,
            anchor_x="center",
            anchor_y="center"
        )
        # Clear the screen
        self.clear()
        arcade.draw_lrwh_rectangle_textured(0, 0, 1412, 868, self.background)
        self.manager.draw()



