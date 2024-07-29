import socket
import threading
import json

host = 'server'
#port = 8020

def send_message(client_socket):
    while True:
        message = input('Enter message: ')
        
        data = {'message': message}
        data_str = json.dumps(data)
        
        if message.lower() == 'exit':
            break
        try:
            client_socket.sendall(bytes(data_str,encoding="utf-8"))
        except socket.error as e:
            print(str(e))
            break
        
def receive_message(client_socket):
    while True:
        try:
            data = client_socket.recv(1024)
            data_dict = json.loads(data.decode("utf-8"))
            print(f"Received message: {data_dict['message']}")
        except socket.error as e:
            print(str(e))
            break

def main():
    port = int(input('Enter port: '))
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, port))
    
    thread_send = threading.Thread(target=send_message, args=(s,))
    thread_receive = threading.Thread(target=receive_message, args=(s,))
    
    thread_send.start()
    thread_receive.start()
    
    thread_send.join()
    
    s.close()

    
if __name__ == '__main__':
    main()