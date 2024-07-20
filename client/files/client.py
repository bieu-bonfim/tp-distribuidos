import socket

def udp_client(message, hostname):
    try:
        # Cria um socket UDP
        a_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        
        # Converte a mensagem para bytes
        message_bytes = message.encode()
        
        # HOSTNAME == IP
        server_address = (hostname, 8000)
        
        # Envia a mensagem para o servidor
        a_socket.sendto(message_bytes, server_address)
        
        # Prepara um buffer para a resposta
        buffer_size = 1000
        buffer = bytearray(buffer_size)
        
        # Recebe a resposta do servidor
        reply, _ = a_socket.recvfrom(buffer_size)
        
        print("Reply:", reply.decode())
    except socket.error as e:
        print("Socket error:", e)
    except Exception as e:
        print("Error:", e)
    finally:
        # Fecha o socket
        a_socket.close()

if name == "main":
    import sys
    #coloca aqui o IP do servidor
    data = ["ola mundo", "0.0.0.1"]
    udp_client(data[0], data[1])