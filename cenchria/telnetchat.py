import server as cserver

class Client(cserver.Client):
    def handleIncomingData(self, data):
        self.manager.sendToAll(data, self)

if __name__ == '__main__':
    runner = cserver.CommandLineRunner()
    runner.server.clientManager.makeClient = lambda s, h, p: Client(s, h, p)
    runner.run()
