#!/usr/bin/env python3

import socketserver
import threading
import bottle
import time

from logger import TerminalLogger
from server_communication import ConfigSyncHandler

DEBUG = True


class ConfigSyncServer(socketserver.TCPServer):
    def __init__(self, ip: str = ConfigSyncHandler.ip, port: int = ConfigSyncHandler.port, web_port: int = 8080, handler_class=ConfigSyncHandler):
        self.web_port = web_port
        self.logger = TerminalLogger(file_path=__file__.replace('py', 'log'))
        self.logger.debug(f'server init: {ip}:{port}')
        try:
            socketserver.TCPServer.__init__(self, (ip, port-1), handler_class)  # non-daemonised (first instance)
        except OSError:
            socketserver.TCPServer.__init__(self, (ip, port), handler_class)  # daemonised (second instance)

    def start_web_loop(self):
        bottle.run(host=ConfigSyncHandler.ip, port=self.web_port, reloader=DEBUG)


def main():
    @bottle.route('/')
    def index():
        short_config = ''
        for c in ConfigSyncHandler.configs.configs:
            short_config += f'<form action="/modify_time_left" method="post"> {c.user if c.user else c.ip}:\t{c.time_left_min}' \
                            f'<input name="+10" value="+10" type="submit"/>' \
                            f'<input name="-10" value="-10" type="submit"/>' \
                            f'<input name="BAN" value="BAN" type="submit"/>' \
                            f'</form>'
        return f'''
        <meta http-equiv="refresh" content="60">
        {short_config}
        '''

    @bottle.post('/modify_time_left')
    def add_time():
        if bottle.request.forms.get('+10'):
            ConfigSyncHandler.configs.configs[0].time_left_today += 600
        elif bottle.request.forms.get('-10'):
            ConfigSyncHandler.configs.configs[0].time_left_today -= 600
        elif bottle.request.forms.get('BAN'):
            ConfigSyncHandler.configs.configs[0].time_left_today = 0

        bottle.redirect("/")

    @bottle.route('/debug')
    def debug():
        ful_configs = ''
        for c in ConfigSyncHandler.configs.configs:
            ful_configs += '<br>'.join(str(c).split(', ')) + '<br><br><br>'
        return f'''
        <meta http-equiv="refresh" content="60">
        {ful_configs}
        '''

    s = ConfigSyncServer()
    t = threading.Thread(target=s.serve_forever)
    t.setDaemon(True)
    t.start()
    s.start_web_loop()


if __name__ == "__main__":
    main()
