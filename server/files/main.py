from server import Server
import threading

def main():
    
    server = Server()
    threading.Thread(target=server.serverStart).start()
    print('Server started')
        
if __name__ == '__main__':
    main()