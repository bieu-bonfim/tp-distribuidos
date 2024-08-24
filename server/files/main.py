from network.PyroServer import PyroServer

def main():
    server = PyroServer()
    server.startServer(ns_host='0.0.0.0', ns_port=8020)
        
if __name__ == '__main__':
    main()