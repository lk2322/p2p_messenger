import random
import time
from threading import Thread


class A:
    def __init__(self):
        self.a = [0]

a = [3]

def foo():
    a.append(random.random())

AA = A()
for i in range(5):
    Thread(foo()).start()

print(a)
