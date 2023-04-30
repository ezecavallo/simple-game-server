"""Server"""

import socket
from threading import Thread, Lock
import json

# Lobby
from rooms import Lobby

# Exceptions
from exceptions import (RoomDoesNotExist, PlayerDoesNotExist,
                        PlayerAlreadyInARoomException,
                        RoomFullException, PlayerNotInRoom)


class TcpServer(Thread):
    """Tcp server"""

    def __init__(self, port, rooms=None):
        Thread.__init__(self)
        self.sock = None

        self.port = int(port)
        self.is_listening = True
        self.rooms = rooms

    def run(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind(("0.0.0.0", self.port))
        print('Bind Ready...')
        self.sock.listen(1)
        print('Listening...')

        while self.is_listening:

            try:
                conn, addr = self.sock.accept()
            except socket.timeout:
                continue

            data = conn.recv(1024)

            print('Conexion desde: '+str(addr))
            parsed_data = json.loads(data)
            self.router(conn, addr, parsed_data)

            conn.close()

        self.sock.close()

    def router(self, conn, addr, data):
        """
        Route received packets based on actions
        """
        action = data.get("action", None)
        identifier = data.get("identifier", None)
        payload = data.get("payload", None)

        if action == 'register':
            client = self.rooms.register(addr, int(payload))
            self.send_tcp(conn, True, client.identifier)
            return

        if not identifier:
            raise Exception()

        if not payload:
            pass

        if action == 'create':
            room_id = self.rooms.create(payload)
            self.send_tcp(conn, True, room_id)
            return

        if action == 'get_rooms':
            rooms_list = self.rooms.to_dict()
            self.send_tcp(conn, True, rooms_list)
            return

        if action == 'join':
            try:
                self.rooms.join(identifier, payload)
            except RoomDoesNotExist:
                self.send_tcp(conn, False, "Room does not exist.")
            except PlayerDoesNotExist:
                self.send_tcp(conn, False)
            except PlayerAlreadyInARoomException:
                self.send_tcp(conn, False)
            except RoomFullException:
                self.send_tcp(conn, False, "Room is full.")

            self.send_tcp(conn, True, payload)
            return

        if action == 'leave_room':
            try:
                self.rooms.leave_room(identifier, payload)
            except PlayerDoesNotExist:
                self.send_tcp(conn, False)
            except RoomDoesNotExist:
                self.send_tcp(conn, False)
            except PlayerNotInRoom:
                self.send_tcp(conn, False)
            self.send_tcp(conn, True, None)
            return

        if action == 'leave':
            try:
                self.rooms.leave(identifier, payload)
            except PlayerDoesNotExist:
                self.send_tcp(conn, False)
            self.send_tcp(conn, True, None)
            return

    def send_tcp(self, conn, success, data=""):
        """Send TCP packet"""

        message = json.dumps({"success": success, "message": data})
        conn.send(message.encode())


if __name__ == '__main__':
    host = '127.0.0.1'
    port = 5001

    rooms = Lobby(2)
    tcp_server = TcpServer(port, rooms)
    tcp_server.start()
