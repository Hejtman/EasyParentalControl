#!/usr/bin/env python3

import socketserver
import logging
import threading


class ConfigSyncHandler(socketserver.BaseRequestHandler):
    def __init__(self, request, client_address, server):
        self.logger = logging.getLogger('ConfigSyncHandler')
        self.logger.debug(f'__init__: {client_address} {server}')
        socketserver.BaseRequestHandler.__init__(self, request, client_address, server)

    def handle(self):
        data = self.request.recv(1024).strip()
        self.logger.info(f'received from {self.client_address[0]}:\n{data}')
        self.request.send(data)


class ConfigSyncServer(socketserver.TCPServer):
    def __init__(self, server_address, handler_class=ConfigSyncHandler):
        self.logger = logging.getLogger('ConfigSyncServer')
        socketserver.TCPServer.__init__(self, server_address, handler_class)
        self.logger.debug(f'__init__: {self.server_address}')


def main():
    logging.basicConfig(level=logging.DEBUG)
    server = ConfigSyncServer(('localhost', 9999), ConfigSyncHandler)
    t = threading.Thread(target=server.serve_forever)
    t.setDaemon(True)  # don't hang on exit
    t.start()


def test():
    import socket
    logger = logging.getLogger('client')
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    logger.debug('connecting to server')
    s.connect(('localhost', 9999))
    s.send(b'1234')
    print(s.recv(1024))
    s.close()


if __name__ == "__main__":
    main()
