import Pyro5.api
from app.LobbyManager import LobbyManager
from app.AuthManager import AuthManager
from app.InventoryManager import InventoryManager
from app.GameManager import GameManager
from app.DeckManager import DeckManager
import sqlite3

@Pyro5.api.expose
class GameMembrane:
    def __init__(self, client, lobbyManager, db_conn):
        self.client = client
        self.lobbyManager = LobbyManager(self.db_conn)
        self.db_conn = db_conn
        self.authManager = AuthManager(self.db_conn)
        self.inventoryManager = InventoryManager(self.db_conn)
        self.gameManager = GameManager(self.db_conn)
        self.deckManager = DeckManager(self.db_conn)

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
        saved_deck = self.deckManager.editDeck(self.deck_id, self.cards)
        saved_deck_data = saved_deck["data"]
        saved_deck_result = saved_deck["status"]
        print(f"Choose deck result: {saved_deck_result}")
        return saved_deck_data if saved_deck_result == "success" else 0
    
    def choose_deck(self):
        choosed_deck = self.deckManager.choose_deck(self.client, self.deck_id)
        choosed_deck_data = choosed_deck["data"]
        choosed_deck_result = choosed_deck["status"]
        print(f"Choose deck result: {choosed_deck_result}")
        return choosed_deck_data if choosed_deck_result == "success" else 0
    
    def start_game(self):#nao sei se o index tá certo
        game = self.lobbyManager.startGame(self.index, self.db_conn)["response"]
        game_data = game["data"]
        game_result = game["status"]
        print(f"Start game result: {game_result}")
        return game_data if game_result == "success" else 0
    
    def play_card(self):
        playCard = self.gameManager.playCard(self.client.id, self.cardName)["response"]
        playCard_data = playCard["data"]
        playCard_result = playCard["status"]
        print(f"Start game result: {playCard_result}")
        return playCard_data if playCard_result == "success" else 0
    
    def choose_stat(self):#nao sei se o stat ta certo
        stat = self.gameManager.setAttribute(self.client.id, self.stat)["response"]
        stat_data = stat["data"]
        stat_result = stat["status"]
        print(f"Choose stat result: {stat_result}")
        return stat_data if stat_result == "success" else 0
    
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