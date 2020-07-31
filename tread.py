import _thread as thread, time

def contador(meuID, cont):
    for i in range(cont):
        time.sleep(1)
        print('[%s] -> %s' % (meuID, i))

for i in range(2):
    thread.start_new_thread(contador,(i,2))

time.sleep(6)
print('Saindo da thread principal')