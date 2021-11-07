#!/usr/bin/env python3

import socketserver
import threading
import time

from logger import TerminalLogger
from server_communication import ConfigSyncHandler


class ConfigSyncServer(socketserver.TCPServer):
    def __init__(self, ip: str = ConfigSyncHandler.ip, port: int = ConfigSyncHandler.port, handler_class=ConfigSyncHandler):
        self.logger = TerminalLogger(file_path=__file__.replace('py', 'log'))
        self.logger.debug('server init')
        socketserver.TCPServer.__init__(self, (ip, port), handler_class)


def main():
    server = ConfigSyncServer()
    t = threading.Thread(target=server.serve_forever)
    t.setDaemon(True)  # don't hang on exit
    t.start()

    while True:
        time.sleep(1)  # TODO: start WEB


if __name__ == "__main__":
    main()
