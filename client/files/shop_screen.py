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
FACE_DOWN_IMAGE = "/home/cards/backcard.jpg"
CARD_SCALE = 0.2

host = 'server'
port = 8020
s = None

class Card(arcade.Sprite):
    """ Card sprite """

    def __init__(self,name, scale=CARD_SCALE):
        """ Card constructor """

        # Attributes for suit and value
        self.name = name

        # Image to use for the sprite when face up
        self.image_file_name = f"/home/cards/{name}.jpg"
        self.is_face_up = False

        # Call the parent
        super().__init__(FACE_DOWN_IMAGE, scale, hit_box_algorithm="None")

    def faceUp(self):
        self.texture = arcade.load_texture(self.image_file_name)
        self.is_face_up = True

    def faceDown(self):
        self.texture = arcade.load_texture(FACE_DOWN_IMAGE)
        self.is_face_up = False

    def isFaceUp(self):
        if self.is_face_up == True:
            return True
        else:
            return False

    @property
    def isFaceDown(self):
        return not self.is_face_up

class ShopScreen(arcade.View):
    """ Main application class. """

    def __init__(self,game_server, session, coin):
        super().__init__()
        self.game_server = game_server
        self.session_id = session
        self.client = game_server.get_client(session)
        self.manager = arcade.gui.UIManager()
        self.manager.enable()
        self.coin = coin
        self.new_cards = None
        self.card_list = None
        self.have_new_cards = False
        # Create a vertical BoxGroup to align buttons
        self.v_box = arcade.gui.UIBoxLayout()

        voltar_menu = arcade.gui.UIFlatButton(text="Comprar Booster", width=200)
        self.v_box.add(voltar_menu.with_space_around(bottom=20))
        voltar_menu.on_click = self.on_click_comprar

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

    def setup(self):
        self.card_list = arcade.SpriteList()

    def on_click_comprar(self, event):
        if self.coin < 10:
            print('Não há moedas suficientes')
        else:
            self.new_cards = self.game_server.buy_booster(self.client)
            self.have_new_cards = True


    def on_click_voltar(self, event):
        menu = main_menu.MainMenu(self.game_server, self.session_id)
        self.window.show_view(menu)

    def on_draw(self):
        """ Render the screen. """
        self.clear()
        arcade.draw_lrwh_rectangle_textured(0, 0, 1412, 868, self.background)
        self.manager.draw()
        self.card_list.draw()
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
        if self.have_new_cards:
            count = 0
            for card_name in self.new_cards:
                if count ==3:
                    count = 0
                card = Card(card_name, CARD_SCALE)
                card.position = (MIDDLE_X - 140) + (140*count), MIDDLE_Y
                self.card_list.append(card)
                count += 1
                card.faceUp()
            self.coin  -= 10
        self.have_new_cards = False



    def receive_message(self):
        while True:
            try:
                self.data_dict = self.client.receiveMessage()
                print(self.data_dict)
                
                if self.data_dict['header'] == 'buy_booster':
                    data = {'header': 'ACK', 'request': {}}
                    self.client.sendMessage(data)
                    self.new_cards = self.data_dict['response']['cards']
                    self.have_new_cards = True
                    break
            except Exception as e:
                print(str(e))