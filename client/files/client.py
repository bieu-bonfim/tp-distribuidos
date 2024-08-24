import socket
import threading
import json
import time

class Client():
    def __init__(self):
        self.client_id = None
        self.client_name = None
        self.client_email = None
        self.client_deck = 0
        self.selected_deck_cards = None