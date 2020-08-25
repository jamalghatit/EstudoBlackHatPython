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
    if receive_first: #1 Faz-se uma verificação para garantir que não precisaremos iniciar uma conexão com o lado remoto e solicitar dados antes de entrar no laço principal
                         #Alguns daemos servidores esperam que voce faça isso previamente ( servidores FTP normalmente enviam um banner antes, por exemplo).
        
        remote_buffer = receive_from(remote_socket) #2 Essa simplesmente recebe um objeto socket conectado e realiza uma recepção dos dados
        hexdump(remote_buffer) #3 Faz-se um dump do conteúdo do pacote para inspecioná-lo e ver se há algo interessante
        
        #envia os dados ao nosso handler de resposta
        remote_buffer = response_handler(remote_buffer) #4 aqui voce poderá modificar o conteúdo do pacote, realizar tarefas de fuzzing, testar aspectos relacioados à autenticação
                                                           # ou o que desejar. 
        
        #se houver dados para serem enviados ao nosso cliente local, envia-os
        if len(remote_buffer):
            print(("[<==] Sending %d bytes to localhost") % len(remote_buffer))
            client_socket.send(remote_buffer)
    # agora vamos entrar no laço e ler do host local,
    # enviar para o host remoto, enviar para o host local, 
    # enxaguar, lavar e repetir.
    
    while True:
        
        # lê do host local
        local_buffer = receive_from(client_socket)
        
        if len(local_buffer):
            
            print("[==>] Received %d bytes from localhost. " % len(local_buffer))
            hexdump(local_buffer)
            
            #envia os dados para nosso handler de solicitações
            local_buffer = request_handler(local_buffer)
            
            # envia os dados ao host remoto
            remote_socket.send(local_buffer)
            print("[==>] Sent to remote")
            
        # recebe a resposta
        remote_buffer = receive_from(remote_socket)
        
        if len(remote_buffer):
            
            print("[<==] Received %d bytes from remote." % len(remote_buffer))
            hexdump(remote_buffer)
            
            #envia dados ao nosso handler de resposta
            remote_buffer = response_handler(remote_buffer)
            
            #envia a resposta para o socket local
            client_socket.send(remote_buffer)
            
            print("[<==] Sent to localhost.")
            
        # Se não houver mais dados em nenhum dos lados, encerra as conexões
        
        if not len(local_buffer) or not len(remote_buffer): #5
            client_socket.close()
            remote_socket.close()
            print("[<==] No more data. Closing connections.")
            
            break

def hexdump(src, length=16):
    result = []
    digits = 4 if isinstance(src, str) else 2  
    # isinstance = passar como primeiro parametro a variavel que deseja validar e como segundo parâmetro o "tipo"
    #Em python3 testa str, não testa unicode, como se fazia em python2
    
    for i in range(0, len(src), length):
        # xrange() gera um elemento de cada vez, o range() gera uma lista contendo todos os elementos, aloca memoria e depois passa para o laço for. Isso é para Python 2
        # Python 3 xrange  -> range()
        s = src[i:i+length]
        # A função ord() retorna um inteiro que representa o caractere Unicode.
        hexa = b' '.join(["%0*X" % (digits, ord(x)) for x in s])
        #  '%*.*f' % (5, 2, 122.71827878) ->  122.72
        text = b''.join([x if 0x20 <= ord(x) < 0x7F else b'.' for x in s])
        result.append(b'%04X %-*s %s' % (i, length*(digit+1), hexa, text))
        # '%-10s texto' % ('test') ->    test       texto
        # %04X ->  número em hexadecimal com 4 casas
        
    print(b'\n '.joint(result))
        
        # str.join() é um método de a str, e intercala essa string entre os argumentos fornecidos.
        # Portanto, quando você executa some_separator.join([a, b, c]), obtém, de fato a + some_separator + b + some_separator + c
        # Exemplo: 'x '.join(['a','b','c']) -> resultado =  'ax/ bx/ c'
    
def receive_from(connection):
    buffer = ''
    
    #definimos um timeout de 2s; de acordo com seu alvo, pode ser que esse valor price ser ajustado
    connection.settimeout(2)    
   
main()