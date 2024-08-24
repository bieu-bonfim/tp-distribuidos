import Pyro5.api
from network.ClientHandler import ClientHandler
import sqlite3

@Pyro5.api.expose
class PyroServer:
    def __init__(self):
        self.db_conn = sqlite3.connect('database/cryptid.db', check_same_thread=False)
        self.daemon = Pyro5.api.Daemon(host='server')
        self.clientHandler = ClientHandler(self.db_conn, self.daemon)

    def startServer(self, ns_host, ns_port):
        with self.daemon as daemon:
            try:
                ns = Pyro5.api.locate_ns(host=ns_host, port=ns_port)
            except Pyro5.errors.NamingError as e:
                print(f"Could not locate the NameServer: {e}")
                return

            server_uri = daemon.register(self)
            ns.register("cryptids.server", server_uri)
            
            game_uri = daemon.register(self.clientHandler)
            ns.register("cryptids.game", game_uri)
            
            daemon.requestLoop()
        
