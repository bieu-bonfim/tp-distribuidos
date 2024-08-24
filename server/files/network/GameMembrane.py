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
        print('GameFacade initialized!')

    def create_lobby(self, client_id):
        lobby_id = self.lobbyManager.create_lobby(client_id)
        return f"Lobby {lobby_id} created by client {client_id}"

    def join_lobby(self, client_id, lobby_id):
        success = self.lobbyManager.join_lobby(client_id, lobby_id)
        return f"Client {client_id} joined lobby {lobby_id}" if success else "Failed to join lobby"

    def login(self, username, password):
        login = self.authManager.login(username, password, self.client)["response"]
        user_data = login["data"]
        login_result = login["status"]
        print(f"Login result: {login_result}")
        return user_data["user_id"] if login_result == "success" else 0