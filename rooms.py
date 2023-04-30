"""Rooms"""

import uuid

#  Player
from player import Player

# Exceptions
from exceptions import (RoomDoesNotExist, PlayerDoesNotExist,
                        PlayerAlreadyInARoomException,
                        RoomFullException, PlayerNotInRoom)


class Lobby:
    """
    Lobby
    """

    def __init__(self, capacity=2):
        self.rooms = {}
        self.players = {}
        self.room_capacity = capacity

    def register(self, addr, port):
        """
        Register new player
        """
        for player in self.players.values():
            print(player.tcp_addr)
            if player.tcp_addr == addr:
                return player

        player = Player(addr, port)
        self.players[player.identifier] = player

        return player

    def create(self, room_name=None):
        """
        Create a new room
        """

        identifier = str(uuid.uuid4())
        self.rooms[identifier] = Room(identifier, self.room_capacity, room_name)

        return identifier

    def join(self, player_id, room_id):
        """
        Add player to a room
        """

        room = self.rooms.get(room_id, None)
        player = self.players.get(player_id, None)

        if not room:
            raise RoomDoesNotExist()

        if not player:
            raise PlayerDoesNotExist()

        if player.room_id:
            raise PlayerAlreadyInARoomException()

        if room.is_full():
            raise RoomFullException()

        room.join(player)

    def get_rooms(self):
        """
        Get rooms
        """

        return self.to_dict()

    def leave_room(self, player_id, room_id):
        """
        Remove player from a room
        """

        if player_id not in self.players:
            raise PlayerDoesNotExist()

        room = self.rooms.get(room_id, None)

        if not room:
            raise RoomDoesNotExist()

        # if player.room_id != room_id:
        #     raise DataInconsistencyException()

        room.leave(player_id)

    def leave(self, player_id, room_id):
        """
        Remove player from lobby/server
        """

        if room_id:
            self.leave_room(player_id, room_id)

        if player_id not in self.rooms:
            self.rooms.pop(player_id, None)

    def to_dict(self):
        """
        Return rooms to dict
        """
        rooms = []
        for room in self.rooms:
            rooms.append({
                "id": room.identifier,
                "room_name": room.room_name,
                "capacity": room.capacity,
                "players": len(room.players),
            })
        return rooms


class Room:
    """
    Room
    """

    def __init__(self, identifier, capacity, room_name=None):

        self.players = []
        self.identifier = identifier
        self.capacity = capacity
        self.room_name = room_name

    def is_player_in_room(self, player_id):
        """
        Check if a player is in a room
        """

        return player_id in self.players

    def is_full(self):
        """Check if room is full"""

        return len(self.players) >= self.capacity

    def join(self, player):
        """
        Join player to room
        """

        if not self.is_full:
            self.players.append(player)
            player.room_id = self.identifier
        else:
            raise RoomFullException()

    def leave(self, player):
        """
        Remove player from room
        """

        if player not in self.players:
            raise PlayerNotInRoom()

        self.players.pop(player)
