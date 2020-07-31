import os

def filho():
    print('ola do filho'.os.getpid())
    os.exit(0)
def pai():
    while True:
        newpid = os.fork()
        if newpid == 0:
            filho()
        else:
            print("ola do pai", os.getpid(), newpid)
        if input() == 'q':
            print("Fechando o pai", os.getpid())
            break

pai()