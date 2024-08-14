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


class ShopScreen(arcade.View):
    """ Main application class. """

    def __init__(self, client, coin):
        super().__init__()
        self.client = client
        self.manager = arcade.gui.UIManager()
        self.manager.enable()
        self.coin = coin
        # Create a vertical BoxGroup to align buttons
        self.v_box = arcade.gui.UIBoxLayout()

        voltar_menu = arcade.gui.UIFlatButton(text="Comprar Booster", width=200)
        self.v_box.add(voltar_menu.with_space_around(bottom=20))
        voltar_menu.on_click = self.on_click_voltar

        voltar_menu = arcade.gui.UIFlatButton(text="Voltar", width=200)
        self.v_box.add(voltar_menu.with_space_around(bottom=20))
        voltar_menu.on_click = self.on_click_voltar



        self.background = arcade.load_texture("/home/sprites/loja_screen.png")

        # Create a widget to hold the v_box widget, that will center the buttons
        self.manager.add(
            arcade.gui.UIAnchorWidget(
                anchor_x="center_x",
                anchor_y="center_y",
                align_y=-300,
                child=self.v_box)
        )

    def on_click_comprar(self, event):

        print("comprar")

    def on_click_voltar(self, event):
        menu = main_menu.MainMenu(self.client)
        self.window.show_view(menu)

    def on_draw(self):
        """ Render the screen. """
        self.clear()
        arcade.draw_lrwh_rectangle_textured(0, 0, 1412, 868, self.background)
        self.manager.draw()
        arcade.draw_rectangle_filled(160, 50, 200, 50, arcade.color.EERIE_BLACK)
        arcade.draw_rectangle_outline(160, 50, 200, 50, arcade.color.ENGLISH_VIOLET)
        arcade.draw_text(
            "Moedas: " + str(self.coin),
            start_x= 160,
            start_y= 50,
            color=arcade.color.WHITE,
            font_size=18,
            anchor_x="center",
            anchor_y="center"
        )


