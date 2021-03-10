"""
Ferramenta em Python do utilitário WHOIS

Ainda em implementação.
"""

import socket
import sys

domain = str(input('digite o site que deseja saber informações: \n'))
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('whois.iana.org', 43))
try:
    s.send((domain + "\r\n").encode("utf-8"))
except IndexError:
    print(
        """
        Digite o site alvo\r
        Exemplo de uso:\r
        whois.py businesscorp.com.br
        """)
    sys.exit()

answer_bytes = s.recv(1024).decode(encoding='latin-1').split()
whois = answer_bytes[19]
s.close()

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((whois, 43))
s.send((domain + "\r\n").encode("utf-8"))
answer_bytes = s.recv(1024).decode(encoding='latin-1')

print(answer_bytes)

