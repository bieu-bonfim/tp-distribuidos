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
        print('Pyro5 Server iniciado!')

    def startServer(self, ns_host='127.0.0.1', ns_port=8020):
        daemon = Pyro5.api.Daemon()

        try:
            ns = Pyro5.api.locate_ns(host=ns_host, port=ns_port)
        except Pyro5.errors.NamingError as e:
            print(f"Could not locate the NameServer: {e}")
            return

        uri = daemon.register(self)
        ns.register("cryptids.server", uri)

        print("Server Pyro iniciado.")
        daemon.requestLoop()
        
    def add_client(self, username, password):
        new_client = Client(self.lobbyManager, self.db_conn, username, password)
        if new_client.id == 0:
            print(f"Client failed to connect.")
            return False
        if new_client not in self.clients:
            self.clients.append()
            print(f"New client connecting")
            return True
        print(f"Client already connected")
        return False

    def connect_client(self, username, password):
        if self.add_client(username, password):
            print( f"Client connected successfully.")
            return True
        print( f"Client failed to connect.")