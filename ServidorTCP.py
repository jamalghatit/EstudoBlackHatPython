import socket
import threading

bind_ip = '0.0.0.0'
bind_port = 9999

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server.bind((bind_ip,bind_port))

server.listen(5)

print("[*] Listening on %s: %d" % (bind_ip,bind_port))

def handle_client(client_socket):
    #exibe o que o cliente enviar
    request = client_socket.recv(1024)
    resposta = request.decode()
    print('[*] Received: %s ' % resposta)

    mensagem = "ACK!"
    msgByte = mensagem.encode()
    #envia um pacote de volta
    client_socket.send(msgByte)
   
    client_socket.close()


while True:
    client, addr = server.accept()
    print("[*] Accepted connection from %s:%d " % (addr[0],addr[1]))
    cliente_handler = threading.Thread(target=handle_client, args=(client,))
    cliente_handler.start()


