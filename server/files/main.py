from network.SocketServer import SocketServer
import threading

def main():
    
    server = SocketServer()
    threading.Thread(target=server.serverStart).start()
    print('Server started')
        
if __name__ == '__main__':
    main()