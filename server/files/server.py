import socket
import threading
import json

clients = []

def broadcast_message(sender, data_dict):
    try:
        for client in clients:
            if client != sender:
                client.sendall(bytes(json.dumps(data_dict), encoding="utf-8"))
    except socket.error as e:
        print(str(e))
        

def handle_client(client_socket):
    with client_socket:
        while True:
            try:
                data = client_socket.recv(1024)
                data_dict = json.loads(data.decode("utf-8"))
                #
                # manipulação dos dados com o json recebido já convertido
                #
                broadcast_message(client_socket, data_dict)
            except socket.error as e:
                print(str(e))
                break
        
def serve():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('0.0.0.0', 8020))
    s.listen()
    while True:
        conn, addr = s.accept()
        clients.append(conn)
        print(f'Connected to {addr}')
        threading.Thread(target=handle_client, args=(conn,), daemon=True).start()
        
if __name__ == '__main__':
    serve()