#!/usr/bin/env python3

import socketserver
import logging
import threading
import pickle

from configs import PersistentConfigs


# TODO file logger
class ConfigSyncHandler(socketserver.BaseRequestHandler):
    def __init__(self, request, client_address, server):
        self.logger = logging.getLogger('ConfigSyncHandler')
        self.logger.setLevel(logging.DEBUG)
        self.logger.debug(f'__init__: {client_address} {server}')
        self.configs = PersistentConfigs()
        socketserver.BaseRequestHandler.__init__(self, request, client_address, server)

    def handle(self):
        time_spend = pickle.loads(self.request.recv(1024).strip())  # FIXME: {client: time_spend}
        self.logger.info(f'time_spend received from {self.client_address[0]}: {time_spend} {type(time_spend)}')
        self.configs.configs[0] += time_spend
        self.logger.info(f'sending back {self.client_address[0]}: {self.configs.configs}')
        self.request.send(pickle.dumps(self.configs.configs))


class ConfigSyncServer(socketserver.TCPServer):
    def __init__(self, server_address, handler_class=ConfigSyncHandler):
        self.logger = logging.getLogger('ConfigSyncServer')
        self.logger.setLevel(logging.DEBUG)
        socketserver.TCPServer.__init__(self, server_address, handler_class)
        self.logger.debug(f'__init__: {self.server_address}')


def main():
    logging.basicConfig(level=logging.DEBUG)
    server = ConfigSyncServer(('localhost', 9999))
    t = threading.Thread(target=server.serve_forever)
    t.setDaemon(True)  # don't hang on exit
    t.start()


if __name__ == "__main__":
    main()
