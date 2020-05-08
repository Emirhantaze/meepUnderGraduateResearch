from threading import Thread
from time import sleep
a = 0
def t():
    global a
    while True:
        a = input()
Thread(target=t).start()
i = 0
olda = 1
while True:
    if((a!=olda)):
        print(a)
    olda=a
    sleep(0.01)
