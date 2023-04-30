"""Exceptions"""


class RoomDoesNotExist(Exception):
    pass


class PlayerDoesNotExist(Exception):
    pass


class PlayerNotInRoom(Exception):
    pass


class PlayerAlreadyInARoomException(Exception):
    pass


class RoomFullException(Exception):
    pass
