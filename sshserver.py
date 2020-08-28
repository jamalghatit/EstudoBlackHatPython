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
        