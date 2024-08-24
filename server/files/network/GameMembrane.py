import Pyro5.api
from app.LobbyManager import LobbyManager
from app.AuthManager import AuthManager
from app.InventoryManager import InventoryManager
import sqlite3

@Pyro5.api.expose
class GameMembrane:
    def __init__(self, client, lobbyManager, db_conn):
        self.client = client
        self.lobbyManager = lobbyManager
        self.db_conn = db_conn
        self.authManager = AuthManager(self.db_conn)
        self.inventoryManager = InventoryManager(self.db_conn)

    def create_lobby(self):
        create = self.lobbyManager.createLobby(self.client)["response"]
        lobby_data = create["data"]["lobby"]
        lobby_result = create["status"]
        print(f"Lobby creation result: {lobby_result}")
        return lobby_data["index"] if lobby_result == "success" else 0
    
    def join_lobby(self, lobby_id):
        join = self.lobbyManager.joinLobby(self.client, lobby_id)["response"]
        lobby_data = join["data"]["lobby"]
        lobby_result = join["status"]
        print(f"Lobby join result: {lobby_result}")
        return lobby_data["index"] if lobby_result == "success" else 0
    
    def load_inventory(self):
        inventory = self.inventoryManager.showUserInventory(self.client.id)["response"]
        inventory_data = inventory["data"]
        inventory_result = inventory["status"]
        print(f"Inventory load result: {inventory_result}")
        return inventory_data if inventory_result == "success" else []
    
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
        booster = self.inventoryManager.buyBooster(self.client.id)["response"]
        booster_result = booster["status"]
        booster_data = booster["data"]
        print(f"Booster purchase result: {booster_result}")
        return booster_data if booster_result == "success" else 0
    
    def login(self, username, password):
        login = self.authManager.login(username, password, self.client)["response"]
        user_data = login["data"]
        login_result = login["status"]
        print(f"Login result: {login_result}")
        return user_data["user_id"] if login_result == "success" else 0