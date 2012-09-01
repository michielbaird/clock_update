import struct
import socket

from threading import Lock
from datetime import datetime
from collections import defaultdict

class IdMismatch(Exception):
    pass
class ErrorMismatch(Exception):
    pass

class ClockUnit:
    GET_TIME_AND_DATE = 0xe5
    SET_TIME_AND_DATE = 0xe6
    locks = defaultdict(Lock)

    def __init__(self, host_id):
        self.active = False
        self.ip_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.host_id  = host_id

    def _buildILV(self,identifier, value):
        if value == "":
            return struct.pack("=BH", identifier, 0)
        else:
            return struct.pack("=BHs", identifier, len(value), value)

    def _unpackILV(self, ilv):
        size = len(ilv) - 3
        print repr(ilv)
        i,l = struct.unpack("=BH", ilv[:3])
        v = ilv[3:]
        return i, v


    def _open(self):
        if not self.active:
            self.ip_socket.connect( self.host_id )
            self.active = True


    def _close(self):
        self.ip_socket.close()
        self.ip_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.active = False



    def _sendAndReceive(self, ilv, close=True):
        self._open()
        start = 0
        while start < len(ilv):
            start += self.ip_socket.send(ilv[start:])
        ilv_rec = self.ip_socket.recv(3)
        i , l = struct.unpack("=BH", ilv_rec)
        print l
        remaining = l
        ilv_rec += self.ip_socket.recv(remaining)
        if close:
            self._close()
        return ilv_rec


    def getDateTime(self):
        ClockUnit.locks[self.host_id].acquire()
        ilv = self._buildILV(ClockUnit.GET_TIME_AND_DATE, "")
        print repr(ilv)
        result = self._sendAndReceive(ilv)
        id, value = self._unpackILV(result)
        if id != ClockUnit.GET_TIME_AND_DATE:
            raise ID_MISMATCH()
        error = struct.unpack("=B", value[0])[0]
        response = value[1:]
        print error, repr(response)
        if error != 0:
            raise ErrorMismatch()
        dow, year, month, day, hour, minute, second = \
                            struct.unpack("=BBBBBBB", response)
        print  dow, year, month, day, hour, minute, second

        ClockUnit.locks[self.host_id].release()
        return datetime(year+2000, month, day, hour, minute, second)


