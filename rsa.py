import asyncio
from typing import Tuple
from Crypto.PublicKey import RSA
from aiomisc import threaded, threaded_separate


class Keys:

    def __init__(self, len_stack: int = 3):
        self.keys = []
        for i in range(len_stack):
            self.__keygen()

    def get_keys(self) -> Tuple[bytes, bytes]:
        """
        Returns a key pair

        Raise IndexError if the keys did not have time to be created
        :return: Tuple(Private key, Public key)
        """

        keys = self.keys.pop()
        self.__keygen()
        return keys

    @threaded
    def __keygen(self) -> None:
        """
        Generate a public / private key pair and writes it as a tuple in self.keys
        """
        key_obj = RSA.generate(2048)
        key_priv = key_obj.export_key('DER')
        key_pub = key_obj.public_key().export_key('DER')
        self.keys.append((key_priv, key_pub))
