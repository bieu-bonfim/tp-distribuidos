import socket
import threading
import time as t

class Connection(threading.Thread):
    clients = []

    def __init__(self, client_socket):
        threading.Thread.__init__(self)
        self.client_socket = client_socket
        Connection.clients.append(self)

    def run(self):
        data = self.client_socket.recv(1024).decode()
        print(f"mensage: {data}")
        self.send(data)


        # TO TRABALHANDO NESSA PARTE
        #aguardar antes de remover da lista de conectados
        #t.sleep(10)
        #self.client_socket.close()
        #Connection.clients.remove(self)

        #self.client_socket.sendall(data.encode())

    def send(self, message):
        for client in Connection.clients:
            if client != self:
                print(f"Olha a mensageeem: {message}")
                client.client_socket.sendall(message.encode())


def start_server():


    server_port = 8020
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('0.0.0.0', server_port))
    server_socket.listen(5)
    print("Server listening on port", server_port)


    while True:
        client_socket, _ = server_socket.accept()
        connection = Connection(client_socket)
        connection.start()

if __name__ == "__main__":
    start_server()