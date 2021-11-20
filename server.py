#!/usr/bin/env python3

import socketserver
import threading
import bottle

from logger import TerminalLogger
from server_communication import ConfigSyncHandler

DEBUG = True
NAME = 'Easy Parental Control'


class ConfigSyncServer(socketserver.TCPServer):
    def __init__(self, ip: str = ConfigSyncHandler.server_ip, port: int = ConfigSyncHandler.server_port, web_port: int = 8080, handler_class=ConfigSyncHandler):
        self.web_port = web_port
        self.logger = TerminalLogger(file_path=__file__.replace('py', 'log'))
        self.logger.debug(f'server init: {ip}:{port}')
        try:
            socketserver.TCPServer.__init__(self, (ip, port-1), handler_class)  # non-daemonised (first instance)
        except OSError:
            socketserver.TCPServer.__init__(self, (ip, port), handler_class)  # daemonised (second instance)

    def start_web_loop(self):
        bottle.run(host=ConfigSyncHandler.server_ip, port=self.web_port, reloader=DEBUG)


def main():
    @bottle.route('/')
    def index():
        short_config = ''
        for i, c in enumerate(ConfigSyncHandler.configs.configs):
            short_config += f'''
                <form action="/modify_time_left" method="post"><font size="5">{c.user if c.user else c.client_ip}:\t{c.time_left_min}</font>
                    <input name="{i}+10" value="+10" type="submit" style="font-size:50px"/>
                    <input name="{i}-10" value="-10" type="submit" style="font-size:50px"/>
                    <input name="{i}BAN" value="BAN" type="submit" style="font-size:50px"/>
                </form>'''
        return f'<meta http-equiv="refresh" content="60"><H1>{NAME}</H1>{short_config}'

    @bottle.post('/modify_time_left')
    def add_time():
        for i, c in enumerate(ConfigSyncHandler.configs.configs):
            if bottle.request.forms.get(f'{i}+10'):
                c.time_left_today += 600
            elif bottle.request.forms.get(f'{i}-10'):
                c.time_left_today -= 600
            elif bottle.request.forms.get(f'{i}BAN'):
                c.time_left_today = 0

        bottle.redirect("/")

    @bottle.route('/debug')
    def debug():  # TODO: set users name?
        ful_configs = ''
        for c in ConfigSyncHandler.configs.configs:
            ful_configs += '<br>'.join(str(c).split(', ')) + '<br><br><br>'
        return f'<meta http-equiv="refresh" content="60"><H1>{NAME}</H1>{ful_configs}'

    s = ConfigSyncServer()
    t = threading.Thread(target=s.serve_forever)
    t.daemon = True
    t.start()
    s.start_web_loop()


if __name__ == "__main__":
    main()
