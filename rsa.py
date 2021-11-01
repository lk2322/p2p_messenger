from threading import Thread
from typing import Tuple
from Crypto.PublicKey import RSA
import asyncio


def threaded(func):
    def wrapper(*args):
        th = Thread(target=func, args=args)
        th.start()
    return wrapper


class Keys:
    def __init__(self, len_stack:int = 3):
        self.keys = []
        for i in range(len_stack):
            self.keygen()
    def get_keys(self) -> Tuple[bytes, bytes]:
        """
        Returns a key pair

        Raise IndexError if the keys did not have time to be created
        :return: Tuple(Private key, Public key)
        """

        keys = self.keys.pop()
        self.keygen()
        return keys

    @threaded
    def keygen(self) -> None:
        """
        Generate a public / private key pair and writes it as a tuple in self.keys
        """
        key_obj = RSA.generate(2048)
        key_priv = key_obj.export_key()
        key_pub = key_obj.public_key().export_key()
        self.keys.append((key_priv, key_pub))
