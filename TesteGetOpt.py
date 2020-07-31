import getopt, sys

optlist, args = getopt.getopt(sys.argv[1:],'n:i:')
for opção, argumento in optlist:
    if opção == '-n':
        nome = argumento
    elif opção == '-i':
        idade = argumento
print(f'{nome} tem {idade} anos')