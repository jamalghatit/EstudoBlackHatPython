import socket

target_host = 'localhost'
target_port = 9999

#cria um objeto socket

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#faz o cliente se conectar
client.connect((target_host,target_port))

msg = 'Connection done, good Job!'
msgByte = msg.encode()

#envia alguns dados
client.send(msgByte)

#recebe alguns dados
response = client.recv(8096)
print(responde.decode())
