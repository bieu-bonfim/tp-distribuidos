import json
from app.AuthManager import AuthManager
from app.GameManager import GameManager
from app.InventoryManager import InventoryManager
from app.DeckManager import DeckManager
import time as t
import sqlite3

class RequestHandler:
    def __init__(self, client, socket_server):
        self.client = client
        self.socket_server = socket_server
        self.db_conn = sqlite3.connect('database/cryptid.db')
        self.authManager = AuthManager(self.db_conn)
        self.gameManager = GameManager(self.db_conn)
        self.inventoryManager = InventoryManager(self.db_conn)
        self.deckManager = DeckManager(self.db_conn)

    def handleRequest(self):
        while True:
            try:    
                t.sleep(3)
                data = self.client.conn.recv(1024).decode("utf-8")
                request = json.loads(data)
                self.socket_server.db_semaphore.acquire()
                response = self.handleRequestType(request)
                self.socket_server.sendMessage(self.client.conn, response)
            except Exception as e:
                print(str(e))
                break
            finally:
                self.socket_server.db_semaphore.release()
                
    def handleRequestType(self, request):
        header = request['header']
        body = request['request']
        result = {'header': 'invalid message'}
        print(request)
        
        if header == 'login':
            result = self.authManager.login(body['username'], body['password'])
        elif header == 'logout':
            result = self.authManager.logout(body['username'])
        elif header == 'register':
            result = self.authManager.register(body['username'], body['password'], body['email'])
        elif header == 'create_lobby':
            result = self.socket_server.lobbyManager.createLobby(self.client)
        elif header == 'available_lobbies':
            result = self.socket_server.lobbyManager.getAvailableLobbies()
        elif header == 'join_lobby':
            result = self.socket_server.lobbyManager.joinLobby(self.client, int(body['index']))
        elif header == 'leave_lobby':
            result = self.socket_server.lobbyManager.leaveLobby(self.client)
        elif header == 'start_game':
            result = self.gameManager.startGame(self.client.current_lobby)
            self.socket_server.broadcastMessageToLobby(self.client.current_lobby, {'header': 'start_game', 'response': {'status': 'success', 'message': 'Jogo iniciado!'}})
        elif header == 'play_card':
            result = self.gameManager.playCard(self.client.current_lobby, body['card_id'])
            self.socket_server.broadcastMessageToLobby(self.client.current_lobby, {'header': 'start_game', 'response': {'status': 'success', 'message': 'Carta enviada!'}})
        elif header == 'end_game':
            result = self.gameManager.endGame(self.client.current_lobby)
            self.socket_server.broadcastMessageToLobby(self.client.current_lobby, {'header': 'start_game', 'response': {'status': 'success', 'message': 'Jogo encerrado!'}})
        elif header == 'manage_inventory':
            result = self.inventoryManager.showUserInventory(body['user_id'])
        elif header == 'add_card_to_inventory':
            result = self.inventoryManager.addCardToInventory(body['user_id'], body['card_id'])
        elif header == 'edit_deck':
            result = self.deckManager.editDeck(body['deck_id'], body['cards'])
        
        return result