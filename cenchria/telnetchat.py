import cenchria.server

class Client(cenchria.server.Client):
    def handleIncomingData(self, data):
        print(data)

class ClientManager(cenchria.server.ClientManager):
    def clientJoined(self, socket, host, port):
        return Client(socket, host, port)
