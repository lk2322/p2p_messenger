from Crypto.PublicKey import RSA
import time


def keygen():
    return RSA.generate(2048)

a = keygen()
start = time.time_ns()
print(a.export_key('DER'))
print(a.public_key().export_key('DER'))
print(time.time_ns() - start)