import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('0.0.0.0', 8020))
s.listen()
conn, addr = s.accept()
with conn:
    print('Connected by', addr)
    while True:
        data = conn.recv(1024)
        if data.decode() == 'exit':
            break
        wait = input(f'Received {data.decode()}, what is the answer: ')
        conn.sendall(wait.encode())