#!/usr/bin/env python3

import guizero

from logger import TerminalLogger
from unix import Unix
from utils import conditional_action
from client_communication import ClientCommunication


class App(guizero.App):
    def __init__(self):
        self.logger = TerminalLogger(file_path=__file__.replace('py', 'log'))
        self.server = ClientCommunication()
        self.configuration = self.server.sync_configuration(time_spend=0)

        # GUI
        super().__init__(title=self.configuration.user, layout='grid')
        self.time_text = guizero.Text(self, text='', size=60, font="Times New Roman", color="lightblue", align='top', grid=[0, 0])
        self.set_main_window(window_width=150, window_height=100)
        self.repeat(1000*self.configuration.loop_time, self.main_loop)  # loop_time seconds to ms for repeat

    def set_main_window(self, window_width, window_height, title_bar_size=30) -> None:
        self.tk.geometry(f'{window_width}x{window_height}+{self.tk.winfo_screenwidth() - window_width}+{self.tk.winfo_screenheight() - window_height - title_bar_size}')  # bottom right
        self.tk.attributes('-alpha', 0.5)  # half transparent
        self.tk.attributes('-topmost', 1)  # always on top
        self.tk.protocol("WM_DELETE_WINDOW", lambda: None)  # un-closable
        self.process_time_left()

    def process_time_left(self) -> None:
        if not self.configuration.server_connected:
            icon = '🔌'
        elif self.configuration.time_left_today <= 0:
            icon = '☠️'
            conditional_action(condition=Unix.is_running(self.configuration.process), action=Unix.kill, process=self.configuration.process)
        elif self.configuration.time_left_today < self.configuration.warning_time:
            icon = '⏰'
            conditional_action(condition=Unix.is_running(self.configuration.process), action=self.show)  # show the main window (in case it was hidden)
        else:
            icon = ''

        self.time_text.value = f'{icon}{self.configuration.time_left_min}'

    def main_loop(self):
        self.configuration = self.server.sync_configuration(time_spend=self.configuration.loop_time if Unix.is_running(self.configuration.process) else 0)
        self.logger.debug(f'spend/limit = {self.configuration.time_left_today} / {self.configuration.daily_limit}')
        self.process_time_left()


def main() -> None:
    app = App()
    app.logger.info(f'Started {60*"-"}')
    app.logger.set_terminal_logging(verbosity=3)  # DEBUG
    app.display()


if __name__ == '__main__':
    main()
