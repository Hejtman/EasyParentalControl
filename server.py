#!/usr/bin/env python3

import socketserver
import threading
import bottle
import daemon

from logger import TerminalLogger
from server_communication import ConfigSyncHandler
from server_web_home import home
from server_web_config import config


class ConfigSyncServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    def __init__(self, ip: str = ConfigSyncHandler.server_ip, port: int = ConfigSyncHandler.server_port, web_port: int = 8080, handler_class=ConfigSyncHandler):
        self.web_port = web_port
        self.logger = TerminalLogger(file_path=__file__.replace('py', 'log'))
        self.logger.debug(f'server init: {ip}:{port}')
        self.logger.info(f'handling {port}')
        socketserver.TCPServer.__init__(self, (ip, port), handler_class)

    def start(self):
        self.handle_conf_requests()
        self.start_web_loop()

    def handle_conf_requests(self):
        self.logger.debug('Starting handling config sync requests.')
        t = threading.Thread(target=self.serve_forever)
        t.daemon = True
        t.start()
        self.logger.debug('Handling config sync requests.')

    def start_web_loop(self):
        self.logger.debug(f'Starting handling web config manipulation:{ConfigSyncHandler.server_ip}:{self.web_port}')
        b = bottle.Bottle()
        b.merge(home)
        b.merge(config)
        b.run(host=ConfigSyncHandler.server_ip, port=self.web_port)
        self.logger.debug('Stopped handling web config manipulation.')


def main():
    with daemon.DaemonContext():
        s = ConfigSyncServer()
        s.start()


if __name__ == "__main__":
    main()
