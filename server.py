#!/usr/bin/env python3

import os
import socketserver
import threading
import bottle
import daemon
import signal
import atexit

from logger import TerminalLogger
from server_communication import ConfigSyncHandler
from server_web_home import home
from server_web_config import config


class ConfigSyncServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    def __init__(self,
                 ip: str = ConfigSyncHandler.server_ip,
                 port: int = ConfigSyncHandler.server_port,
                 web_port: int = 8080,
                 handler_class: classmethod = ConfigSyncHandler) -> None:
        self.web_port = web_port
        self.pid_file = __file__.replace('py', 'pid')
        self.logger = TerminalLogger(file_path=__file__.replace('py', 'log'))
        self.logger.debug(f'server init: {ip}:{port}')
        self.logger.info(f'handling {port}')
        socketserver.TCPServer.__init__(self, (ip, port), handler_class)

    def start(self) -> None:
        self.create_pid_file()
        atexit.register(self.die)
        self.handle_sync_config_requests()
        self.start_web_config_loop()

    def die(self) -> None:
        self.logger.debug('Terminating.')
        os.remove(self.pid_file)

    def stop(self) -> None:
        try:
            with open(self.pid_file, 'r') as f:
                pid = int(f.read().strip())
                os.kill(pid, signal.SIGTERM)
        except FileNotFoundError:
            print('Server is not running.')
        except OSError:
            print(f'Server is dead ({self.pid_file}).')

    def create_pid_file(self):
        with open(self.pid_file, 'w') as f:
            f.write(str(os.getpid()))

    def handle_sync_config_requests(self):
        self.logger.debug('Starting handling config sync requests.')
        t = threading.Thread(target=self.serve_forever)
        t.daemon = True
        t.start()
        self.logger.debug('Handling config sync requests.')

    def start_web_config_loop(self):
        self.logger.debug(f'Starting handling web config manipulation:{ConfigSyncHandler.server_ip}:{self.web_port}')
        b = bottle.Bottle()
        b.merge(home)
        b.merge(config)
        b.run(host=ConfigSyncHandler.server_ip, port=self.web_port)  # blocking operation!
        self.logger.debug('Stopped handling web config manipulation.')


def main():
    # todo parse command line > start / stop
    with daemon.DaemonContext(signal_map={signal.SIGTERM: 'terminate'}):
        ConfigSyncServer().start()


if __name__ == "__main__":
    main()
