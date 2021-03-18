import socket, json, select
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

    def connect(self, remoteIP, remotePort):
        pass

    def disConnect(self):
        pass

    def sendMessage(self, message):
        pass

    def hasPending(self):
        pass

    def reciveMessage(self):
        pass

    IP = property(lambda self: self._IP, lambda self, ip: self._setIP(ip))
    PORT = property(lambda self: self._Port, lambda self, port: self._setPort(port))

class Client(commModule):
    def __init__(self):
        self._Sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._MSGSPan = 1024

        self._QIN = Queue()
        self._QOut = Queue()
        self._Daemon = None

    def connect(self, ip, port):
        self._Sock.connect((ip, port))
        self._Daemon = Thread(target=self._worker)
    
    def disConnect(self):
        self._QOut.put('EXIT')
        self._Daemon.join()
        self._Daemon = None

        self._Sock.close()

    def _serialize(self, message):
        return bytes(super()._serialize(message))

    def _deserialize(self, message):
        return super()._deserialize(message.decode('utf-8'))

    def sendMessage(self, message):
        self._QOut.put(self._serialize(message))

    def hasPending(self):
        return not self._QIN.empty()

    def reciveMessage(self):
        if not self._QIN.empty():
            msg = self._QIN.get()

            if isinstance(msg, Exception):
                raise msg
            
            return self._deserialize(msg)

    def _worker(self):
        exe = True
        while exe:
            try:
                if not self._QOut.empty():
                    msg = self._QOut.get()

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

class Server(commModule):
    def __init__(self):
        self._Sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._MSGSPan = 1024

        self._QIN = Queue()
        self._QOut = Queue()
        self._Daemon = None

    def connect(self, bindIP, bindPort, maxClient=5):
        self._Sock.bind((bindIP, bindIP))
        self._Sock.listen(maxClient)
        self._Daemon = Thread(target=self._worker)

    def disConnect(self):
        self._QOut.put('EXIT')
        self._Daemon.join()
        self._Daemon = None

        self._Sock.close()

    def _serialize(self, message):
        return bytes(super()._serialize(message))

    def _deserialize(self, message):
        return super()._deserialize(message.decode('utf-8'))

    def sendMessage(self, message, client):
        self._QOut.put([client, self._serialize(message)])

    def hasPending(self):
        return not self._QIN.empty()

    def reciveMessage(self):
        if not self._QIN.empty():
            msg = self._QIN.get()

            if isinstance(msg, Exception):
                raise msg
            
            return self._deserialize(msg[1]), [0]

    def _worker(self):
        exe = True
        clients = [self._Sock]
        while exe:
            try:
                if not self._QOut.empty():
                    msg = self._QOut.get()

                    if msg == 'EXIT':
                        exe = False
                    elif msg[0] in clients:
                        msg[0].sendall(msg[1])

                pending, waiting, exceptional = select.select(clients, clients, clients)
            
                for cli in pending:
                    if cli is self._Sock:
                        connection, address = cli.accept()
                        connection.setblocking(0)
                        clients.append(connection)
                    else:
                        msg = ''

                        while True:
                            data = cli.recv(self._MSGSPan)

                            if len(data) <= 0:
                                break
                            else:
                                msg += data
                        if len(msg) <= 0:
                            clients.remove(cli)
                            cli.close()
                        else:
                            self._QIN.put([cli, msg])

                for cli in exceptional:
                    clients.remove(cli)
                    cli.close()
            
            except Exception as e:
                self._QIN.put(e)
    

