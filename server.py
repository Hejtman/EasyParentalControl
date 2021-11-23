#!/usr/bin/env python3

import socketserver
import threading
import bottle

from logger import TerminalLogger
from server_communication import ConfigSyncHandler
from server_web_home import home
from server_web_config import config

DEBUG = True  # FIXME: CLI or environ?


class ConfigSyncServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    allow_reuse_address = True

    def __init__(self, ip: str = ConfigSyncHandler.server_ip, port: int = ConfigSyncHandler.server_port, web_port: int = 8080, handler_class=ConfigSyncHandler):
        self.web_port = web_port
        self.logger = TerminalLogger(file_path=__file__.replace('py', 'log'))
        self.logger.debug(f'server init: {ip}:{port}')
        try:
            socketserver.TCPServer.__init__(self, (ip, port-1), handler_class)  # non-daemonised (first instance)
        except OSError:
            socketserver.TCPServer.__init__(self, (ip, port), handler_class)  # daemonised (second instance)

    def start_web_loop(self):
        b = bottle.Bottle()
        b.merge(home)
        b.merge(config)
        b.run(host=ConfigSyncHandler.server_ip, port=self.web_port, reloader=DEBUG)


def main():
    s = ConfigSyncServer()
    t = threading.Thread(target=s.serve_forever)
    t.daemon = True
    t.start()
    s.start_web_loop()


if __name__ == "__main__":
    main()
