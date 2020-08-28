import threading
import paramiko
import subprocess

def ssh_command(ip, user, passwd, command): #1 função que estabelece uma conexão com um servidor SSH e executa um único comando
    client = paramiko.SSHClient()
    #client.load_host_keys('/home/justin/.ssh/known_hosts') #2 o Paramiko suporta autenticação com chaves
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy()) #3 Define-se a politica que aceite a chave ssh do servidor SSH para o qual estamos conectando
    client.connect(ip, username=user, password = passwd)
    ssh_session = client.get_transport().open_session()
    if ssh_session.active:
        ssh_session.exec_command(command)
        print(ssh_session.recv(1024))
    return 


ssh_command('192.168.80.128','kali', 'kali', 'id')