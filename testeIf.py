x = 2.1
y = 4 if isinstance(x, int) else 15



def hexdump(src, length=16):
    result = []
    digits = 4 if isinstance(src, str) else 2  
    # isinstance = passar como primeiro parametro a variavel que deseja validar e como segundo parâmetro o "tipo"
    #Em python3 testa str, não testa unicode, como se fazia em python2
    
    for i in range(0, len(src), length):
        # xrange() gera um elemento de cada vez, o range() gera uma lista contendo todos os elementos, aloca memoria e depois passa para o laço for. Isso é para Python 2
        # Python 3 xrange  -> range()
        s = src[i:i+length]
        # A função ord() retorna um inteiro que representa o caractere Unicode.
        hexa = b' '.join(["%0*X" % (digits, ord(x)) for x in s])
        text = b''.join([x if 0x20 <= ord(x) < 0x7F else b'.' for x in s])
        result.append(b'%04X %-*s %s' % (i, length*(digit+1), hexa, text))
    print (b'\n '.joint(result))
        
        # str.join() é um método de a str, e intercala essa string entre os argumentos fornecidos.
        # Portanto, quando você executa some_separator.join([a, b, c]), obtém, de fato a + some_separator + b + some_separator + c
        # Exemplo: 'x '.join(['a','b','c']) -> resultado =  'ax/ bx/ c'
    
i = 17
length = 10
digit = 4
hexa = "hexa"
text = "text"
# print('%04X %-*s %s' % (i, 50, hexa, text))


print( '%*.*f' % (5, 2, 122.71827878))