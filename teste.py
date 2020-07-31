def f1():
    a = 3
    def f3():
        nonlocal a
        a+=1
        print('o valor de a é {}'.format(a))
    def f4():
        global a 
        a+=1
        print('o valor de a é {}'.format(a))
    f3()
    f4()

a = 10   
f1()
