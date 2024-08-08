import socket
import threading
import time
import client
import json
import login
import arcade
import arcade.gui
from arcade import load_texture
from arcade.gui import UIManager
from arcade.gui.widgets import UITextArea, UIInputText, UITexturePane

class EditDeck(arcade.View):
    def __init__(self):
        super().__init__()

        self.manager = arcade.gui.UIManager()
        self.manager.enable()

        self.v_box = arcade.gui.UIBoxLayout()

        self.scrollable_view = None

    def on_draw(self):
        self.clear()
        self.manager.draw()
    def on_mouse_press(self, x, y, button, modifiers):
        if self.button.check_mouse_press(x, y):
            print("Clicado!")

    def on_show_view(self):
        self.manager.enable()

    def on_hide_view(self):
        self.manager.disable()
