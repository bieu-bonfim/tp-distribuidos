from network.PyroServer import PyroServer

def main():
    server = PyroServer()
    server.startServer('pyro-ns', 8020)
        
if __name__ == '__main__':
    main()