from PySock.PySock import Server

ser = Server()
ser.connect('127.0.0.1', '5000')

try:
    while True:
        if ser.hasPending():
            msg, cli = ser.reciveMessage()
            print(msg)
            ser.sendMessage(msg, cli)
except KeyboardInterrupt:
    pass
except Exception as e:
    print(e)
finally:
    ser.disConnect()
