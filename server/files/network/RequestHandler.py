import json
from app.AuthManager import AuthManager
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
        self.inventoryManager = InventoryManager(self.db_conn)
        self.deckManager = DeckManager(self.db_conn)

    def handleRequest(self):
        while True:
            try:    
                data = self.client.conn.recv(1024).decode("utf-8")
                request = json.loads(data)
                # self.socket_server.db_semaphore.acquire()
                response = self.handleRequestType(request)
                self.socket_server.sendMessage(self.client.conn, response)
            except Exception as e:
                print(str(e))
                break
            # finally:
            #     self.socket_server.db_semaphore.release()
                
    def handleRequestType(self, request):
        header = request['header']
        body = request['request']
        result = {'header': 'invalid message'}
        print(request)
        
        if header == 'login':
            result = self.authManager.login(body['username'], body['password'])
            self.client.username = body['username']
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
            self.socket_server.broadcastMessageToLobbyOthers(self.client.conn, self.client.current_lobby, result)
        elif header == 'leave_lobby':
            result, result_lobby = self.socket_server.lobbyManager.leaveLobby(self.client)
            self.socket_server.broadcastMessageToLobbyOthers(self.client.conn, self.client.current_lobby, result_lobby)
        elif header == 'choose_deck':
            self.client.current_deck = body['deck_id']
            result = {'header': 'choose_deck', 'response': {'status': 'success', 'message': 'Baralho escolhido!'}}
        elif header == 'start_game':
            result = self.socket_server.lobbyManager.startGame(self.client.current_lobby, self.db_conn)
            self.socket_server.broadcastMessageToLobbyOthers(self.client.conn, self.client.current_lobby, result)
        elif header == 'play_card':
            result = self.socket_server.lobbyManager.lobbyController.lobbies[self.client.current_lobby].gameManager.playCard(self.client, body['name'])
            self.socket_server.broadcastMessageToLobbyOthers(self.client.conn, self.client.current_lobby, result)
        elif header == 'choose_stat':
            result = self.socket_server.lobbyManager.lobbyController.lobbies[self.client.current_lobby].gameManager.chooseStat(self.client, body['stat'])
            self.socket_server.broadcastMessageToLobbyOthers(self.client.current_lobby, {'header': 'choose_stat', 'response': {'status': 'success', 'message': 'Carta enviada!'}})
        elif header == 'end_game':
            result = self.gameManager.endGame(self.client.current_lobby)
            self.socket_server.broadcastMessageToLobbyOthers(self.client.current_lobby, {'header': 'end_game', 'response': {'status': 'success', 'message': 'Jogo encerrado!'}})
        elif header == 'manage_inventory':
            result = self.inventoryManager.showUserInventory(body['user_id'])
        elif header == 'add_card_to_inventory':
            result = self.inventoryManager.addCardToInventory(body['user_id'], body['card_id'])
        elif header == 'edit_deck':
            result = self.deckManager.editDeck(body['deck_id'], body['cards'])
        elif header == 'retrieve_deck':
            result = self.deckManager.retrieveDeck(self.client.current_deck)
        
        print("sending ", result)
        return result