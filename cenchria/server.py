import socket
from select import select

class SocketHandler(object):
    def __init__(self, socket):
        self.socket = socket
    
    def fileno(self):
        return self.socket.fileno()
    
    def shutdown(self, flag=socket.SHUT_WR):
        self.socket.shutdown(flag)
    
    def close(self):
        self.socket.close()

class Client(SocketHandler):
    def __init__(self, socket, host, port):
        SocketHandler.__init__(self, socket)
        self.host = host
        self.port = port
    
    def read(self):
        """Returns true if this socket is still alive, false otherwise"""
        data = self.socket.recv(4096)
        
        if data == "":
            return False
        else:
            self.handleIncomingData(data)
    
    def handleIncomingData(self, data):
        # Override me
        pass

class ServerSocket(SocketHandler):
    def __init__(self):
        SocketHandler.__init__(self, socket.socket(
            socket.AF_INET, socket.SOCK_STREAM))
        
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)        
        
        self.read = []
        self.write = []
        self.errored = []
    
    def configure(self, host, port, acceptQueueLength=10):
        self.socket.bind((host, port))
        self.socket.listen(acceptQueueLength)
    
    def accept(self):
        socket, (host, port) = self.socket.accept()
        return socket, host, port

class ServiceException(Exception):
    pass

class ClientManager(object):
    def __init__(self):
        self.clients = []
    
    def clientJoined(self, socket, host, port):
        client = self.makeClient(socket, host, port)
        self.logClientJoin(client)
        self.clients.append(client)
    
    def makeClient(self, socket, host, port):
        return Client(socket, host, port)
    
    def clientLeft(self, client):
        self.logClientLeave(client)
        self.clients.remove(client)
    
    def closeAll(self):
        for client in self.clients:
            client.close()
    
    def logClientJoin(self, client):
        print("Client joined from %s:%s", (client.host, client.port))
    
    def logClientLeave(self, client):
        print("Client left: %s:%s" % (client.host, client.port))

class Server(object):
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.ssocket = None
        self.acceptQueueLength = 10
        self.stop = False
        self.clientManager = ClientManager()
    
    def run(self):
        if self.ssocket is not None:
            # Server already in use
            raise ServiceException("Server already in use")
        
        # Create an IPv4 server socket
        self.ssocket = ServerSocket()
        self.ssocket.configure(self.host, self.port, self.acceptQueueLength)
        
        self.loop()
    
    def loop(self):
        while not self.stop or self.clientManager.clients:
            read = self.clientManager.clients
            
            if not self.stop:
                # Add the server only if we're not stopping it
                read = read + [self.ssocket]
            
            write = []
            error = []
            readable, writable, errored = select(read, write, error)
            
            for socket in readable:
                if socket is self.ssocket:
                    self.clientManager.clientJoined(*socket.accept())
                else:
                    if not socket.read():
                        # Client left
                        self.clientManager.clientLeft(socket)
    
    def shutdown(self, now=False):
        if now:
            # Do a brutal exit
            self.ssocket.close()
            self.clientManager.closeAll()
        
        else:
            self.stop = True
            
            # Serve remaining clients before exit
            self.loop()
            
            # And finally, close the server socket
            self.ssocket.close()

class CommandLineRunner(object):
    def __init__(self, server):
        self.server = server
    
    def run(self):
        try:
            print("Starting server on 127.0.0.1:8080")
            self.server.run()
        except KeyboardInterrupt:
            try:
                print("\nGraceful shutdown. Hit ^C again to kill")
                self.server.shutdown()
            except KeyboardInterrupt:
                print("\nForce exit")
                self.server.shutdown(now=True)
        except Exception as e:
            import traceback
            traceback.print_exc()
            print e
            
            self.server.shutdown(now=True)

if __name__ == "__main__":
    CommandLineRunner(Server("127.0.0.1", 8080)).run()
