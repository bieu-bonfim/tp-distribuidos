import json
from app.AuthManager import AuthManager
from app.InventoryManager import InventoryManager
from app.DeckManager import DeckManager
import threading
import time as t
import sqlite3

class RequestHandler:
    def __init__(self, client, socket_server):
        self.client = client
        self.socket_server = socket_server
        self.db_conn = sqlite3.connect('database/cryptid.db', check_same_thread=False)
        self.authManager = AuthManager(self.db_conn)
        self.inventoryManager = InventoryManager(self.db_conn)
        self.deckManager = DeckManager(self.db_conn)
        self.ack = False

    def keepSendingMessages(self, response):
        while True:
            t.sleep(1)
            print('------ Mensagem enviada  ------')
            self.socket_server.sendMessage(self.client.conn, response)
            if self.ack:
                print('------ Confirmado o ACK ------')
                self.ack = False
                break
            

    def handleRequest(self):
        while True:
            try:    
                t.sleep(1)
                data = self.client.conn.recv(1024).decode("utf-8")
                request = json.loads(data)
                self.socket_server.db_semaphore.acquire()
                
                if request['header'] == 'ACK':
                    print('------ Mensagem recebida ------')
                    self.ack = True
                    continue
                    
                response = self.handleRequestType(request)
                
                if response['header'] != 'broadcast':
                    threading.Thread(target=self.keepSendingMessages, args=(response,), daemon=True).start()
                    
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
            result = self.authManager.login(body['username'], body['password'], self.client)
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
            print('playing card')
            result = self.socket_server.lobbyManager.lobbyController.lobbies[self.client.current_lobby].gameManager.playCard(self.client, body['card'])
            self.socket_server.broadcastMessageToLobby(self.client.current_lobby, result)
            if result['response']['status'] == 'turn_over':
                t.sleep(3)
                turn_over = self.socket_server.lobbyManager.lobbyController.lobbies[self.client.current_lobby].gameManager.turnOver()
                self.socket_server.broadcastMessageToLobby(self.client.current_lobby, turn_over)
                t.sleep(3)
                resolve_turn = self.socket_server.lobbyManager.lobbyController.lobbies[self.client.current_lobby].gameManager.resolveRound()
                self.socket_server.broadcastMessageToLobby(self.client.current_lobby, resolve_turn)
                if resolve_turn['response']['status'] == 'game_over':
                    t.sleep(3)
                    game_over = self.socket_server.lobbyManager.lobbyController.lobbies[self.client.current_lobby].gameManager.resolveGame()
                    self.socket_server.broadcastMessageToLobby(self.client.current_lobby, game_over)
            self.printGameState()
            return {'header': 'broadcast'}
                
        elif header == 'choose_stat':
            print('choosing stat')
            result = self.socket_server.lobbyManager.lobbyController.lobbies[self.client.current_lobby].gameManager.setAttribute(self.client, body['stat'])
            self.printGameState()
            
            if result['response']['status'] == 'success':
                self.socket_server.broadcastMessageToLobby(self.client.current_lobby, result)
                return {'header': 'broadcast'}
        elif header == 'manage_inventory':
            result = self.inventoryManager.showUserInventory(body['user_id'])
        elif header == 'add_card_to_inventory':
            result = self.inventoryManager.addCardToInventory(body['user_id'], body['card_id'])
        elif header == 'edit_deck':
            result = self.deckManager.editDeck(body['deck_id'], body['cards'])
        elif header == 'retrieve_deck':
            result = self.deckManager.retrieveDeck(self.client.current_deck)
        elif header == 'buy_booster':
            result = self.inventoryManager.buyBooster(self.client)
            
            
        print("sending ", result)
        return result
    
    def printGameState(self):
        print('------ Estado do jogo ------')
        print('Client: ', self.client)
        print('Current deck: ', self.client.current_deck)
        print('Current lobby: ', self.client.current_lobby)
        print('Current turn: ', self.socket_server.lobbyManager.lobbyController.lobbies[self.client.current_lobby].gameManager.current_player)
        print('Round: ', self.socket_server.lobbyManager.lobbyController.lobbies[self.client.current_lobby].gameManager.round)
        print('Round attribute: ', self.socket_server.lobbyManager.lobbyController.lobbies[self.client.current_lobby].gameManager.round_attribute)
        print('Round cards: ', self.socket_server.lobbyManager.lobbyController.lobbies[self.client.current_lobby].gameManager.round_cards)
        print('------ ------ ------ ------')