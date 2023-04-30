"""Player"""

import uuid


class Player:
    """
    Player
    """

    def __init__(self, addr, port):
        self.identifier = str(uuid.uuid4())
        self.room_id = None
        self.tcp_addr = addr
        self.client_server = (addr[0], port)
