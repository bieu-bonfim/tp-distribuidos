import Pyro5.api
from app.LobbyManager import LobbyManager
from app.AuthManager import AuthManager
from app.InventoryManager import InventoryManager
from network.Client import Client
from app.GameManager import GameManager
from app.DeckManager import DeckManager
import time as t
import sqlite3
import Pyro5.api

@Pyro5.api.expose
class ClientHandler:
    def __init__(self, db_conn, daemon):
        self.db_conn = db_conn
        self.daemon = daemon
        self.lobbyManager = LobbyManager()
        self.authManager = AuthManager(self.db_conn)
        self.inventoryManager = InventoryManager(self.db_conn)
        self.deckManager = DeckManager(self.db_conn)
        self.sessions = {}

    def create_lobby(self, client):
        create = self.lobbyManager.createLobby(client)["response"]
        lobby_data = create["data"]["lobby"]
        lobby_result = create["status"]
        print(f"Lobby creation result: {lobby_result}")
        print(f"Lobby data: {lobby_data}")
        return lobby_data if lobby_result == "success" else 0
    
    def join_lobby(self, lobby_id, client):
        print(f"Joining lobby {lobby_id}...")
        join = self.lobbyManager.joinLobby(client, lobby_id)["response"]
        print(f"Join response: {join}")
        lobby_data = join["data"]["lobby"]
        lobby_result = join["status"]
        print(f"Lobby join result: {lobby_result}")
        return lobby_data if lobby_result == "success" else 0
    
    def leave_lobby(self, client):
        self.lobbyManager.leaveLobby(client)
        
    @Pyro5.api.expose
    def load_inventory(self, client):
        print(f"Loading inventory...")
        inventory = self.inventoryManager.showUserInventory(client.get_id())["response"]
        inventory_data = inventory["data"]
        inventory_result = inventory["status"]
        print(f"Inventory load result: {inventory_result}")
        return inventory_data if inventory_result == "success" else []
    
    def save_deck(self, deck_id, cards):
        saved_deck = self.deckManager.editDeck(deck_id, cards)["response"]
        saved_deck_result = saved_deck["status"]
        print(f"Choose deck result: {saved_deck_result}")
        return True if saved_deck_result == "success" else 0
    
    def choose_deck(self, client, deck_id):
        self.deckManager.choose_deck(client, deck_id)
        print('deck selecionado')
    
    def buy_booster(self, client):
        booster = self.inventoryManager.buyBooster(client)["response"]
        booster_result = booster["status"]
        print(f"Booster purchase result: {booster_result}")
        return booster["cards"] if booster_result == "success" else 0
    
    def login(self, username, password):
        client = Client(username)
        login = self.authManager.login(username, password, client)["response"]
        login_result = login["status"]

        print(f"Login result: {login_result}")
        
        if login_result == "success":
            session_id = self.daemon.register(client)
            self.sessions[session_id] = client
            return session_id

    def get_client(self, session_id):
        client = self.sessions.get(session_id, None)
        #print(f"Client retrieved: {client}")
        return client
        
    def register(self, client, client_uri, index):
        self.lobbyManager.register_client(client, Pyro5.api.Proxy(client_uri), index)
        #print(f"Client registered with URI: {client_uri}")

        
    def trigger_lobby_event(self, index, message):
        lobby = self.lobbyManager.lobbyController.getLobby(index)
        for proxy in lobby.proxies:
            if proxy is not None:
                proxy = Pyro5.api.Proxy(proxy._pyroUri)
                print(f"Sending message to {proxy}")
                proxy.receive_event(message)
                
    def trigger_lobby_update(self, index, players):
        lobby = self.lobbyManager.lobbyController.getLobby(index)
        for proxy in lobby.proxies:
            if proxy is not None:
                proxy = Pyro5.api.Proxy(proxy._pyroUri)
                proxy.update_players(players)
                
    def trigger_lobby_start(self, index):
        game = self.lobbyManager.startGame(index, self.db_conn)["response"]
        game_data = game["data"]
        game_result = game["status"]
        if game_result == "success":
            print(f"Start game result: {game_result}")
            lobby = self.lobbyManager.lobbyController.getLobby(index)
            print(f"players: {lobby.player_names}")
            for proxy in lobby.proxies:
                if proxy is not None:
                    print(f"Starting game for {proxy}")
                    proxy = Pyro5.api.Proxy(proxy._pyroUri)
                    proxy.start_game(lobby.player_names)
                    
    def change_to_game(self, index, client, game_screen):
        lobby = self.lobbyManager.lobbyController.getLobby(index)
        player_index = lobby.player_names.index(client.get_username())
        proxy = lobby.proxies[player_index]
        proxy = Pyro5.api.Proxy(proxy._pyroUri)
        print(f"Changing screen to game")
        proxy.set_screen(game_screen)
        
    def load_client_deck(self, client):
        deck = self.deckManager.retrieveDeck(client.get_current_deck())['response']
        if deck['status'] == 'success':
            return deck['data']['deck']['cards']
        
    def play_card(self, cardName, client):
        lobby = self.lobbyManager.lobbyController.getLobby(client.get_current_lobby())
        print(f"Playing card {cardName}...")
        print(f"Current player: {client.get_username()}")
        playCard = lobby.gameManager.playCard(client, cardName)["response"]
        print(f"Play card response: {playCard}")
        print(lobby.gameManager.round_cards)
        if (playCard["status"] == "turn_over"):
            t.sleep(2)
            round_result = lobby.gameManager.resolveRound()["response"]
            if round_result["status"] == "game_over":
                t.sleep(2)
                game_result = lobby.gameManager.resolveGame()["response"]
                return game_result["message"]
            return round_result["message"]
        return playCard["message"]
    
    def choose_stat(self, stat, client):
        lobby = self.lobbyManager.lobbyController.getLobby(client.get_current_lobby())
        stat = lobby.gameManager.setAttribute(client, stat)["response"]
        print(f"Stat chosen: {stat}")
        print(f"Mensagem: {stat['message']}")
        return stat["message"]
        
    def get_played_cards(self, client):
        lobby = self.lobbyManager.lobbyController.getLobby(client.get_current_lobby())
        if lobby.gameManager.round_cards.count(None) == 0:
            pass
        return lobby.player_names, lobby.gameManager.round_cards
    
    def get_chosen_stat(self, client):
        lobby = self.lobbyManager.lobbyController.getLobby(client.get_current_lobby())
        return lobby.gameManager.round_attribute
    
    def clean_for_real(self, client):
        lobby = self.lobbyManager.lobbyController.getLobby(client.get_current_lobby())
        lobby.gameManager.clean_card_vector()
        
    def is_turn_over(self, client):
        lobby = self.lobbyManager.lobbyController.getLobby(client.get_current_lobby())
        return lobby.turnOver 