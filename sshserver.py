import socket
import paramiko
import threading
import sys
# usando a chave dos arquivos de demonstração do paramiko

host_key = paramiko.RSAKey(filename='test_rsa.key') #1
class Server(paramiko.ServerInterface): # This class defines an interface for controlling the behavior of Paramiko in server mode.
    # 2 - 
    def _init_(self):
        self.event = threading.Event()
    def check_channel_request(self, kind, chanid):
        if kind == 'session':
            return paramiko.OPEN_SUCCEEDED # This is one of two standard signal handling options; it will simply perform the default function for the signal.
                                           # For example, on most systems the default action for SIGQUIT is to dump core and exit, while the default action 
                                           # for SIGCHLD is to simply ignore it
        return paramiko.OPEN_FAILED_ADMINISTRATIVELY_PROHIBITED #This is another standard signal handler, which will simply ignore the given sign
    
    def check_auth_password(self, username, password):
        if(username == 'justin') and (password == 'lovesthepython'):
            return paramiko.AUTH_SUCCEEDED
        return paramiko.AUTH_FAILED

server = sys.argv[1]
ssh_port = int(sys.argv[2])

try:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1 )
    sock.bind((server, ssh_port))
    sock.listen(100)
    print("[+] Listening for connection ...")
    client, addr = sock.accept()
except Exception as e:
    print('[-] Listen failed: ' + str(e))
    sys.exit(1)

print('[+] Got a connection!')

try:
    bhSession = paramiko.transport(client)
    # Um transporte SSH se conecta a um fluxo (geralmente um socket), negocia uma sessão criptografada, 
    # autentica e, em seguida, cria túneis de fluxo, chamados canais <.Channel>, na sessão. Vários canais 
    # podem ser multiplexados em uma única sessão (e geralmente são, no caso de encaminhamentos de porta). 
    # As instâncias desta classe podem ser usadas como gerenciadores de contexto.
    bhSession.add_server_key(host_key)
    #Adicione uma chave de host à lista de chaves usadas para o modo de servidor.
    # Ao se comportar como um servidor, a chave do host é usada para assinar determinados pacotes durante a 
    # negociação SSH2, para que o cliente possa confiar que somos quem dizemos ser. Como é usada para assinatura, a                                    
    # chave deve conter informações da chave privada, não apenas a metade pública. Apenas uma chave de cada tipo (RSA ou DSS) é mantida.                                   
    server = Server()
    try:
        bhSession.start_server(server=server)
    except paramiko.SSHException as e:
        print'[-] SSH negotiation failed.'
    chan = bhSession.accept(20)
    print("[+] Authenticated!")
    print(chan.recv(1024))
    chan.send("Welcome to bh_ssh")
    
    while True:
        try:
            command = raw_input("Enter command: ").strip('\n')
            if command !=




        