from PySock.PySock import Client

cli = Client()
cli.connect('127.0.0.1', '5000')

try:
    while True:
        if cli.hasPending():
            print(cli.reciveMessage())

        cli.sendMessage(input('>'))
except KeyboardInterrupt:
    pass
except Exception as e:
    print(e)
finally:
    cli.disConnect()