import socket
import json
from queue import Queue
from threading import Thread

class commModule:
    def __init__(self, ip, port=None):
        self._IP = ip.split(':')[0] if ':' in ip else ip
        self._Port = port if port is not None else ip.split(':')[1] if ':' in ip else None

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

    def sendMessage(self, message, requireRecipt=False, timeout=0):
        pass

    def hasPending(self):
        pass

    def reciveMessage(self, timeout=0):
        pass

    IP = property(lambda self: self._IP, lambda self, ip: self._setIP(ip))
    PORT = property(lambda self: self._Port, lambda self, port: self._setPort(port))

class commClient(commModule):
    def __init__(self, ip, port=None):
        super().__init__(ip, port)
        self._Sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._MSGSPan = 1024

        self._QIN = Queue()
        self._QOut = Queue()
        self._Daemon = None

    def connect(self, remoteIP, remotePort):
        self._Daemon = Thread(target=self._worker)
        self._Sock.connect((remoteIP, remotePort))
    
    def disConnect(self):
        self._QOut.put('EXIT')
        self._Daemon.join()
        self._Daemon = None

        self._Sock.close()

    def _serialize(self, message):
        return bytes(super()._serialize(message))

    def _deserialize(self, message):
        return super()._deserialize(message.decode('utf-8'))

    def sendMessage(self, message, messageType):
        self._Sock.sendall(self._serialize(message))

    def hasPending(self):
        return not self._QIN.empty()

    def reciveMessage(self):
        if not self._QIN.empty():
            msg = self._QIN.get_nowait()

            if isinstance(msg, Exception):
                raise msg
            
            return self._deserialize(msg)

    def _worker(self):
        exe = True
        while exe:
            try:
                if not self._QOut.empty():
                    msg = self._QOut.get_nowait()

                    if msg == 'EXIT':
                        exe = False
                    else:
                        self._Sock.sendall(msg)
            
                msg = ''

                while True:
                    data = self._Sock.recv(self._MSGSPan)

                    if len(data) <= 0:
                        break
                    else:
                        msg += data

                self._QIN.put(msg)
            
            except Exception as e:
                self._QIN.put(e)



            


