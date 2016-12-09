from twisted.internet.protocol import Factory
from twisted.protocols.basic import LineReceiver
from twisted.internet import reactor
class Server(LineReceiver):
	def __init__(self, clientConn):
		self.clientConn = clientConn
		
	def send_data(self, msg):
		self.sendLine(msg + "\n")
		
	def lineReceived(self, line):
		print line
		if line == "supersecretpassword":
			print "Connected to client"
			self.clientConn[0] = self
		elif self.clientConn[0] != None:
			self.clientConn[0].send_data(line)

class ServerFactory(Factory):
	def __init__(self):
		self.clientConn = [None]
	def buildProtocol(self, addr):
		return Server(self.clientConn)
if __name__ == "__main__":
	reactor.listenTCP(9999, ServerFactory())
	reactor.run()