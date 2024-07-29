import socket
import threading

clients = []

def broadcast_message(sender, message):
    try:
        for client in clients:
            if client != sender:
                #client.sendall(f"Broadcasted message: {message} from {sender.getpeername()}".encode())
                client.sendall(f"{message}".encode())
    except socket.error as e:
        print(str(e))
        

def handle_client(client_socket):
    with client_socket:
        while True:
            try:
                data = client_socket.recv(1024)
                if data.decode() == 'exit':
                    clients.remove(client_socket)
                    break
                print(data.decode())
                broadcast_message(client_socket, data.decode())
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