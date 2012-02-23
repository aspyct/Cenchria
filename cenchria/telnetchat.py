import server as cserver

class Client(cserver.Client):
    def handleIncomingData(self, data):
        if len(data) == 1:
            print(ord(data))
        else:
            self.sendToAll(data, self)

if __name__ == '__main__':
    server = cserver.Server("127.0.0.1", 8080)
    
    def makeClient(socket, host, port):
        client = Client(socket, host, port)
        client.sendToAll = server.clientManager.sendToAll
        return client

    server.clientManager.makeClient = makeClient    
    
    cserver.CommandLineRunner(server).run()
