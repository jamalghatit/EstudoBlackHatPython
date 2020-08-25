import sys
import socket
import threading

def server_loop(local_host, local_port, remote_host, remote_port, receive_first):
    
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        server.bind((local_host, local_port))
    except:
        print("[!!] Failed to listen on %s:%d " % (local_host, local_port))
        print("[!!] Check for other listening socket or correct permission.")
        sys.exit(0)
    print("[*] Listening on %s:%d" % (local_host, local_port))
    
    server.listen(5)
    
    while True:
        client_socket, addr = server.accept()
        
        #exibe informações sobre a conexão local
        
        print("[==>] Received incoming connection from %s:%d" % (addr[0], addr[1]))
        
        #inicia uma thread para conversar com o host remoto
        proxy_thread = threading.Thread(target=proxy_handler, args=(client_socket, remote_host, remote_port, receive_first))
        
        proxy_thread.start()

def main():
    # sem parsing sofisticado de linha de comando nesse caso
    if len(sys.argv[1:]) != 5:
        print("Usage: ./proxy.py [localhost] [localport] [remotehost] [remoteport] [receive_first]")
        print("Example: ./proxy.py 127.0.0.1 9000 10.12.132.1 9000 True")
        sys.exit(0)
        
    #define parâmetros para ouvir localmente
    local_host = sys.argv[1]
    local_port = int(sys.argv[2])
    
    # define o alvo remoto
    remote_host = sys.argv[3]
    remote_port = int(sys.argv[4])
    
    #o código a seguir diz ao nosso proxy para conectar e receber dados
    # antes de enviar ao host remoto
    receive_first = sys.argv[5]
    
    if  "True" in receive_first:
        receive_first =  True 
    else:
        receive_first = False
    
    # agora coloca em ação o nosso soquet que ficará ouvindo
    server_loop(local_host, local_port, remote_host, remote_port, receive_first)

def proxy_handler(client_socket, remote_host, remote_port, receive_first):
    # conecta-se ao host remoto
    remote_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    remote_socket.connect((remote_host, remote_port))
    
    #recebe dados do lado remoto, se for necessário
    if receive_first:
        
        remote_buffer = receive_from(remote_socket)
        hexdump(remote_buffer)
        
        #envia os dados ao nosso handler de resposta
        remote_buffer = response_handler(remote_buffer)
        
        #se houver dados para serem enviados ao nosso cliente local, envia-os
        if len(remote_buffer):
            print("[<==] Sending %d bytes to localhost") % len(remote_buffer))
            client_socket.send(remote_buffer)
    # agora vamos entrar no laço e ler do host local,
    # enviar para o host remoto, enviar para o host local, 
    # enxaguar, lavar e repetir.
    
    while True:
        
        # lê do host local
        local_buffer = receive_from(client_socket)
        
        if len(local_buffer):
            
            print
    
    
main()