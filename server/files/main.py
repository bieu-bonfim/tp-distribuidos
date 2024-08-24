from network.PyroServer import PyroServer

def main():
    server = PyroServer()
    server.startServer(ns_host='127.0.0.1', ns_port=8020)
        
if __name__ == '__main__':
    main()