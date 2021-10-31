#!/usr/bin/env python3

import sys
import time
from pathlib import Path
from logger import TerminalLogger

from unix import Unix
from server_api import ServerAPI

sys.path.insert(0, f'{Path.home()}/Library/Python/3.8/lib/python/site-packages')  # FIXME: rather copy source-code to this repo
import guizero


class App(guizero.App):
    def __init__(self):
        self.logger = TerminalLogger(file_path=f'{Path(Path.home(), Path(__file__).stem)}.log')
        self.server = ServerAPI(ip='192.168.1.1')  # FIXME: mv ip to client configuration
        self.configuration = self.server.retrieve_configuration(client=Unix.get_user_name())

        # GUI
        window_width = window_height = 100
        super().__init__(title=self.configuration.user, width=window_width, height=window_height, layout='grid')
        title_bar_size = 30
        self.tk.geometry(f'+{self.tk.winfo_screenwidth() - window_width}+{self.tk.winfo_screenheight() - window_height - title_bar_size}')
        self.time_text = guizero.Text(self, text=self.configuration.time_left_min, size=80, font="Times New Roman", color="lightblue", align='top', grid=[0, 0])
        self.repeat(1000 * self.configuration.loop_time, self.main_loop)

    def warn_if_needed(self) -> None:
        if self.configuration.time_left_sec < self.configuration.warning_time:
            self.logger.info(f'⏰{self.configuration.time_left_sec}')
            self.time_text.value = f'⏰{self.configuration.time_left_sec}'  # FIXME min
        else:
            self.logger.debug(f'⏰{self.configuration.time_left_sec} too soon for {self.configuration.warning_time}s warning.')
            self.time_text.value = self.configuration.time_left_sec  # FIXME min

    def kill_if_needed(self) -> None:
        if self.configuration.time_spend_today > self.configuration.daily_limit:
            if Unix.is_running(self.configuration.process):
                self.logger.info(f'☠️{self.configuration.process}')
                self.time_text.value = f'☠️'
                Unix.kill(process=self.configuration.process)
            else:
                self.logger.debug(f'☠️Noting to kill. {self.configuration.process} is not running.')

    def main_loop(self):
        if Unix.is_running(process=self.configuration.process):
            self.server.report_use(time_spend=self.configuration.loop_time)

        self.configuration = self.server.retrieve_configuration(client=Unix.get_user_name())
        self.logger.debug(f'spend/limit = {self.configuration.time_spend_today} / {self.configuration.daily_limit} ({self.configuration.time_left_sec})')

        self.warn_if_needed()
        self.kill_if_needed()


def main() -> None:
    app = App()
    app.logger.info(f'Started {60*"-"}')
    app.logger.set_terminal_logging(verbosity=3)  # DEBUG
    app.display()


if __name__ == '__main__':
    main()
