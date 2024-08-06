from server.files.classes.client import Client
import threading

def main():
    client = Client()
    threading.Thread(target=client.startClient).start()
    
if __name__ == '__main__':
    main()