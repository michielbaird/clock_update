import struct
import socket

from threading import Lock
from datetime import datetime
from collections import defualtdict

class IdMismatch(Exception):
    pass
class ErrorMismatch(Exception):
    pass

class ClockUnit:
    GET_TIME_AND_DATE = 0xe5
    SET_TIME_AND_DATE = 0xe6
    locks = defualtdict(Lock)

    def __init__(self, host_id):
        self.active = False
        self.ip_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.host_id  = host_id

    def _buildILV(identifier, value):
        return struct.pack("BHp", identifier, len(value), value)

    def _unpackILV(ilv):
        i,l,v = struct.unpack("BHp", ilv)
        return i, v


    def _open(self):
        if not self.active:
            self.ip_socket.connect( self.host_id )
            self.active = True


    def _close(self):
        self.ip_socket.close()
        self.ip_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.active = False



    def _sendAndReceive(self, ilv, close=True)
        self._open()
        start = 0
        while start < len(ilv):
            start += self.ip_socket.send(ilv[start:])
        ilv_rec = self.ip_socket.recv(2)
        remaining = ord(ilv[1])
        ilv_rec += self.ip_socket.recv(remaining)
        if close:
            self._close()
        return ilv_rec


    def getDateTime(self):
        lock.acquire()
        ilv = self._buildILV(GET_TIME_AND_DATE, "")
        result = self._sendAndReceive(ilv)
        id, value = self._unpackILV
        if id != GET_TIME_AND_DATE:
            raise ID_MISMATCH()
        error, response = struct.unpack("BP")
        if error != 0:
            raise ErrorMismatch()
        dow, year, month, day, hour, minute, second =
                            struct.unpack("BBBBBBB", response)
        print  dow, year, month, day, hour, minute, second

        lock.release()
        return datetime(year, month, day, hour, minute, second)


