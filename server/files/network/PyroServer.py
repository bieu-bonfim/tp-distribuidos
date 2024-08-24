import Pyro5.api
from app.LobbyManager import LobbyManager
from network.Client import Client


@Pyro5.api.expose
class PyroServer:
    def __init__(self):
        self.clients = list()
        self.lobbyManager = LobbyManager()
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
