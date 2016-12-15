from twisted.internet.protocol import Factory
from twisted.protocols.basic import LineReceiver
from twisted.internet import reactor
class Server(LineReceiver):
	def __init__(self, clientConn, state):
		self.clientConn = clientConn
		self.state = state
		
	def send_data(self, msg):
		self.sendLine(msg + "\n")
		
	def lineReceived(self, line):
		print line
		if line == "supersecretpassword":
			print "Connected to client"
			self.clientConn[0] = self
			self.state[0] = "Main"
		elif line == "enableboss":
			self.state[0] = "Boss"
		elif line == "showcredits":
			self.state[0] = "Credits"
		elif line == "getstate":
			self.send_data(str(self.state[0]))
		elif self.clientConn[0] != None:
			self.clientConn[0].send_data(line)

class ServerFactory(Factory):
	def __init__(self):
		#these variables are in lists to allow me to pass them by reference into Server and maintain state. They should always only contain 1 value.
		self.clientConn = [None]
		self.state = ["Main"]
	def buildProtocol(self, addr):
		return Server(self.clientConn, self.state)
if __name__ == "__main__":
	reactor.listenTCP(9999, ServerFactory())
	reactor.run()