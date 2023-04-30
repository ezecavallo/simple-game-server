"""Client"""

import socket
from threading import Thread, Lock
import json

host = '127.0.0.1'
port = 5001


# while True:
#     # sock.send("hi".encode("utf-8"))

#     sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#     message = input(" -> ")  # take input
#     if not message:
#         break
#     sock.connect((host, port))
#     sock.send(message.encode("utf-8"))
#     # sock.send(("#"*1020).encode("utf-8"))

#     data = sock.recv(1024).decode("utf-8")
#     print('Received from server: ' + data)  # show in terminal
# sock.close()
# # print('Conexion desde: '+str(addr))


class Client:
    """Client"""

    def __init__(self, server_host, udp_port, tcp_port, client_port):
        self.identifier = None
        self.room_id = None
        self.sock = None

        self.client_server = ("0.0.0.0", client_port)
        self.udp_server = (server_host, udp_port)
        self.tcp_server = (server_host, tcp_port)
        self.listener = ListerSocket(self.client_server, self)
        self.messages = []

        self._register()

    def _send_server(self, message):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect(self.tcp_server)
        self.sock.send(message.encode())
        data = self.sock.recv(1024)
        self.sock.close()

        return data

    def _register(self):
        """
        Register client in server
        """

        message = json.dumps({
            "action": "register",
            "payload": self.client_server[1],
        })
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect(self.tcp_server)
        self.sock.send(message.encode())
        data = self.sock.recv(1024)
        self.sock.close()

        response = self.parse_data(data)
        self.identifier = response

    def create_room(self, room_name):
        """
        Create a new room
        """

        message = json.dumps({
            "action": "create",
            "payload": room_name,
            "identifier": self.identifier,
        })
        data = self._send_server(message)
        response = self.parse_data(data)
        self.room_id = response

    def join(self, room_id):
        """
        Create a new room
        """

        message = json.dumps({
            "action": "join",
            "payload": room_id,
            "identifier": self.identifier,
        })
        data = self._send_server(message)
        response = self.parse_data(data)
        self.room_id = response

    def leave_room(self):
        """
        Leave room
        """

        message = json.dumps({
            "action": "leave_room",
            "payload": self.room_id,
            "identifier": self.identifier,
        })
        data = self._send_server(message)
        response = self.parse_data(data)
        self.room_id = response

    def leave(self):
        """
        Leave room
        """

        message = json.dumps({
            "action": "leave",
            "payload": self.room_id,
            "identifier": self.identifier,
        })
        data = self._send_server(message)
        print(data)
        response = self.parse_data(data)
        self.room_id = response

    def parse_data(self, raw_data):
        """
        Parse data from server
        """

        data = json.loads(raw_data)
        success = data.get("success")

        if success:
            return data["message"]

        raise Exception(data["data"])


class ListerSocket(Thread):
    """UDP client connection"""

    def __init__(self, client_server, client):
        Thread.__init__(self)
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_server = client_server
        self.client = client

    def run(self):
        """
        Get messages from server
        """
        message, _ = self.sock.recvfrom(1024)
        self.client.messages.append(message)

    def stop(self):
        """
        Close socket connection
        """
        self.sock.close()


if __name__ == '__main__':
    host = '127.0.0.1'
    port = 5001

    client1 = Client(host, port, port, port)
    # try:
    #     pass
    # finally:
    # client1.leave()
