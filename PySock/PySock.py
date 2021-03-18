import socket
import json

class commModule:
    def __init__(self, ip, port=none):
        self._IP = ip.split(':')[0] if ':' in ip else ip
        self._Port = port if not port else ip.split(':')[1] if ':' in ip else None

    def _setIP(self, ip):
        self._IP = ip

    def _setPort(self, port):
        self._Port = port

    def _serialize(self, message):
        return json.dumps(message)

    def _deserialize(self, message):
        return json.loads(message)

    def connect(self, remoteIP, remotePort, timeout=0):
        pass

    def disConnect(self):
        pass

    def sendMessage(self, message, requireRecipt=false, timeout=0):
        pass

    def hasPending(self):
        pass

    def reciveMessage(self, timeout=0):
        pass

IP = property(lambda self: self._IP, lambda self, ip: self._setIP(ip))
PORT = property(lambda self: self._Port, lambda self, port: self._setPort(port))