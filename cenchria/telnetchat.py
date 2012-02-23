import server as cserver

class Client(cserver.Client):
    def handleIncomingData(self, data):
        if len(data) == 1:
            print(ord(data))
        else:
            print(data.strip())

if __name__ == '__main__':
    server = cserver.Server("127.0.0.1", 8080)
    server.clientManager.makeClient = lambda s, h, p: Client(s, h, p)
    cserver.CommandLineRunner(server).run()
