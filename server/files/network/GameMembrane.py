import Pyro5.api
from app.LobbyManager import LobbyManager
from app.AuthManager import AuthManager
import sqlite3

@Pyro5.api.expose
class GameMembrane:
    def __init__(self, client, lobbyManager, db_conn):
        self.client = client
        self.lobbyManager = lobbyManager
        self.db_conn = db_conn
        self.authManager = AuthManager(self.db_conn)

    def create_lobby(self):
        create = self.lobbyManager.createLobby(self.client)["response"]
        lobby_data = create["data"]
        lobby_result = create["status"]
        print(f"Lobby creation result: {lobby_result}")
        pass
    
    def join_lobby(self, lobby_id):
        pass
    
    def load_inventory(self):
        pass
    
    def save_deck(self):
        pass
    
    def choose_deck(self):
        pass
    
    def start_game(self):
        pass
    
    def play_card(self):
        pass
    
    def choose_stat(self):
        pass
    
    def buy_booster(self):
        pass
    
    def login(self, username, password):
        login = self.authManager.login(username, password, self.client)["response"]
        user_data = login["data"]
        login_result = login["status"]
        print(f"Login result: {login_result}")
        return user_data["user_id"] if login_result == "success" else 0