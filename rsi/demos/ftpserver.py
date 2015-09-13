from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer

authorizer = DummyAuthorizer()
authorizer.add_user("mini", "mini", "/home/mininet", perm="elradfmw")

handler = FTPHandler
handler.authorizer = authorizer

#server = FTPServer(("127.0.0.1", 21), handler)
server = FTPServer(("192.168.1.203", 21), handler)
server.serve_forever()
