import socketserver
class ThreadedHTTPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass