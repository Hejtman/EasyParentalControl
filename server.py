#!/usr/bin/env python3

import socketserver
import threading
import bottle

from logger import TerminalLogger
from server_communication import ConfigSyncHandler

DEBUG = True


class ConfigSyncServer(socketserver.TCPServer):
    def __init__(self, ip: str = ConfigSyncHandler.ip, port: int = ConfigSyncHandler.port, web_port: int = 8080, handler_class=ConfigSyncHandler):
        self.web_port = web_port
        self.logger = TerminalLogger(file_path=__file__.replace('py', 'log'))
        self.logger.debug('server init')
        socketserver.TCPServer.__init__(self, (ip, port), handler_class)

    def start_web_loop(self):
        bottle.run(host=ConfigSyncHandler.ip, port=self.web_port, reloader=DEBUG)


def main():
    @bottle.route('/')
    def index():
        short_config = ''
        ful_configs = ''
        for c in ConfigSyncHandler.configs.configs:
            short_config += f'<form action="/modify_time_left" method="post"> {c.user if c.user else c.ip}:\t{c.time_left_min} / {c.daily_limit_min}' \
                            f'<input value="+10" type="submit" />' \
                            f'<input value="-10" type="submit" />' \
                            f'</form>'
            ful_configs += '<br>'.join(str(c).split(', ')) + '<br><br><br>'
        return f'''
        <meta http-equiv="refresh" content="60">
        {short_config}
        <br><br><br>{ful_configs}
        '''

    @bottle.post('/modify_time_left')
    def add_time():
        ConfigSyncHandler.configs.configs[0].time_left_today += 600
        bottle.redirect("/")

    server = ConfigSyncServer()
    t = threading.Thread(target=server.serve_forever)
    t.setDaemon(True)  # don't hang on exit
    t.start()
    server.start_web_loop()


if __name__ == "__main__":
    main()
