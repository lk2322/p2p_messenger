import struct
from typing import Union
import hashlib

FMT = '!4s32sH'


class Packet:
    def __init__(self, cmd: str, content: Union[str, bytes]):
        """
        :param cmd:  MESG or NKEY only
        :param content:
        """
        self.cmd = bytes(cmd, 'utf-8')
        if type(content) == bytes:
            self.content = content
        else:
            self.content = bytes(content, 'utf-8')
        self.length = len(self.content)
        # FIXME сделать хаш ДО шифрования сообщений
        self.id = hashlib.sha256(self.content).digest()

    def build(self):
        return struct.pack(FMT, self.cmd, self.id, self.length) + self.content


def unpack_packet(data: bytes) -> list[bytes, bytes, int, bytes]:
    """

    :param data:
    :return: list[command, hash, content_len, content]
    """
    size = struct.calcsize(FMT)
    msg = list(struct.unpack(FMT, data[:size]))
    msg.append(data[size:])
    return msg


if __name__ == '__main__':
    # test
    a = Packet('NKEY', 'asdfsadf')
    b = a.build()
    print(b)
