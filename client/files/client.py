import socket
import sys

def handshake(message, hostname):
    server_port = 8020
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((hostname, server_port))


    client_socket.sendall(message.encode())
    data = client_socket.recv(1024).decode()
    print("Received:", data)

if __name__ == "__main__":
    while True:
        message = input("enter message: ")
        handshake(message, "server")
    #if len(sys.argv) != 3:
    #    print("Usage: python client.py <message> <hostname>")
    #    sys.exit(1)
    #start_client(sys.argv[1], sys.argv[2])