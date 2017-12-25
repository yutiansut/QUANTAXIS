from threading import  Thread,enumerate


def x():
    while True:
        print(1)
Thread(target=x, name='aaa').start()
print(enumerate())
while True:
    print(2)
