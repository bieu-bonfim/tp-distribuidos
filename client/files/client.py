import socket
import threading
import time

host = 'server'
port = 8020

def send_message(client_socket):
    while True:
        message = input('Enter message: ')
        if message.lower() == 'exit':
            break
        try:
            client_socket.sendall(message.encode())
        except socket.error as e:
            print(str(e))
            break
        
def receive_message(client_socket):
    while True:
        try:
            data = client_socket.recv(1024)
            print(f'Received {data.decode()}')
        except socket.error as e:
            print(str(e))
            break

def print_on_timer( ):
    while True:
        print( "Timer Test" )
        time.sleep( 5 )
    

def main():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, port))
    
    thread_send = threading.Thread(target=send_message, args=(s,))
    thread_receive = threading.Thread(target=receive_message, args=(s,))
    thread_print = threading.Thread(target=print_on_timer)
    
    thread_send.start()
    thread_receive.start()
    thread_print.start()
    
    
    thread_send.join()
    
    s.close()

    
if __name__ == '__main__':
    main()