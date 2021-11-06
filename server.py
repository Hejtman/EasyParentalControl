#!/usr/bin/env python3

import socketserver
import logging
import threading

from server_communication import ConfigSyncHandler


class ConfigSyncServer(socketserver.TCPServer):
    def __init__(self, server_address, handler_class=ConfigSyncHandler):
        self.logger = logging.getLogger('ConfigSyncServer')
        socketserver.TCPServer.__init__(self, server_address, handler_class)


def main():
    logging.basicConfig(level=logging.INFO)
    server = ConfigSyncServer(('localhost', 9999))
    t = threading.Thread(target=server.serve_forever)
    t.setDaemon(True)  # don't hang on exit
    t.start()


if __name__ == "__main__":
    main()
