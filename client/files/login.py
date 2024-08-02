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

# Screen title and size
SCREEN_WIDTH = 924
SCREEN_HEIGHT = 868
SCREEN_TITLE = "Cryptids: The Conspiracy"
BASE_MARGIN = 30

class QuitButton(arcade.gui.UIFlatButton):
    def on_click(self, event: arcade.gui.UIOnClickEvent):
        arcade.exit()

class LoginButton(arcade.gui.UIFlatButton):
    def on_click(self, event: arcade.gui.UIOnClickEvent):
        print("bap")


class MyGame(arcade.Window):
    """ Main application class. """

    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)

        self.manager = arcade.gui.UIManager()
        self.manager.enable()

        # Create a vertical BoxGroup to align buttons
        self.v_box = arcade.gui.UIBoxLayout()

        # Again, method 1. Use a child class to handle events.
        quit_button = LoginButton(text="Login", width=200)
        self.v_box.add(quit_button)

        arcade.set_background_color(arcade.color.CHARLESTON_GREEN)

        # Create a widget to hold the v_box widget, that will center the buttons
        self.manager.add(
            arcade.gui.UIAnchorWidget(
                anchor_x="center_x",
                anchor_y="center_y",
                child=self.v_box)
        )

    def setup(self):
        a = 1
        #thread_receive = threading.Thread(target=self.receive_message, args=(s,))
        #thread_receive.start()

        #data = {'header': 'player_connection','player_name_register': player_name}
        #data_str = json.dumps(data)

        #try:
        #    s.sendall(bytes(data_str,encoding="utf-8"))
        #except socket.error as e:
        #    print(str(e))


    def on_click_start(self, event):
        print("Start: ", event )

    def on_draw(self):
        """ Render the screen. """
        # Clear the screen
        self.clear()
        self.manager.draw()

def main():
    """ Main function """
    
    #port = int(input('Enter port: '))

    #s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #s.connect((host, port))


    window = MyGame()
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()