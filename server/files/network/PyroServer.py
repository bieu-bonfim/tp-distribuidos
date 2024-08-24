import Pyro5.api
from app.LobbyManager import LobbyManager
from network.Client import Client
import sqlite3

@Pyro5.api.expose
class PyroServer:
    def __init__(self):
        self.lobbyManager = LobbyManager()
        self.db_conn = sqlite3.connect('database/cryptid.db', check_same_thread=False)
        self.clients = list()

    def startServer(self, ns_host, ns_port):
        with Pyro5.api.Daemon(host='server') as daemon:
            try:
                ns = Pyro5.api.locate_ns(host=ns_host, port=ns_port)
            except Pyro5.errors.NamingError as e:
                print(f"Could not locate the NameServer: {e}")
                return

            uri = daemon.register(self)
            ns.register("cryptids.server", uri)
            daemon.requestLoop()
        
    @Pyro5.api.expose
    def add_client(self, username, password):
        new_client = Client(self.lobbyManager, self.db_conn, username, password)
        if new_client.id == 0:
            print(f"Client failed to connect.")
        if new_client not in self.clients:
            self.clients.append(new_client)
            return new_client.id
        print(f"Client already connected")

    @Pyro5.api.expose
    def connect_client(self, username, password):
        id =  self.add_client(username, password)
        if id != 0:
            print( f"Client connected successfully.")
            return True, self.get_client(id)
        
    @Pyro5.api.expose
    def get_client(self, client_id):
        for client in self.clients:
            if client.id == client_id:
                return client