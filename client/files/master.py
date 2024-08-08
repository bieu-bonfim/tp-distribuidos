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

# Screen title and size
SCREEN_WIDTH = 924
SCREEN_HEIGHT = 868
SCREEN_TITLE = "Cryptids: The Conspiracy"
BASE_MARGIN = 30

def main():


    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    start_view = login.Login()
    window.show_view(start_view)
    arcade.run()
    #return s


if __name__ == "__main__":
    main()